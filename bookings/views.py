from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
import json
import re

from .models import Booking, AdventureEvent, PreRegistration, Payment
from .services import WhatsAppService, PIXService, PaymentService
from users.models import CustomUser
from adventures.models import Adventure

User = get_user_model()


class BookingListView(LoginRequiredMixin, ListView):
    """
    Lista de reservas do usuário
    """
    model = Booking
    template_name = 'bookings/list.html'
    context_object_name = 'bookings'
    login_url = reverse_lazy('users:login')
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related(
            'event__adventure'
        ).order_by('-created_at')


class BookingDetailView(LoginRequiredMixin, DetailView):
    """
    Detalhes de uma reserva
    """
    model = Booking
    template_name = 'bookings/detail.html'
    context_object_name = 'booking'
    login_url = reverse_lazy('users:login')
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related(
            'event__adventure'
        ).prefetch_related('user_checklist__checklist_item')


class BookingCreateView(LoginRequiredMixin, TemplateView):
    """
    Criar nova reserva
    """
    template_name = 'bookings/create.html'
    login_url = reverse_lazy('users:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        context['event'] = get_object_or_404(AdventureEvent, id=event_id)
        return context
    
    def post(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(AdventureEvent, id=event_id)
        
        # Verificar se já tem reserva para este evento
        if Booking.objects.filter(user=request.user, event=event).exists():
            messages.error(request, 'Você já tem uma reserva para este evento.')
            return redirect('adventures:detail', slug=event.adventure.slug)
        
        # Criar reserva
        booking = Booking.objects.create(
            user=request.user,
            event=event,
            participants_count=1,
            total_price=event.final_price,
            status='pending'
        )
        
        messages.success(request, 'Reserva criada com sucesso! Aguarde aprovação.')
        return redirect('bookings:detail', pk=booking.pk)


class BookingCancelView(LoginRequiredMixin, TemplateView):
    """
    Cancelar reserva
    """
    template_name = 'bookings/cancel.html'
    login_url = reverse_lazy('users:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.kwargs.get('pk')
        context['booking'] = get_object_or_404(
            Booking, 
            id=booking_id, 
            user=self.request.user
        )
        return context
    
    def post(self, request, *args, **kwargs):
        booking_id = self.kwargs.get('pk')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        if booking.can_cancel:
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Reserva cancelada com sucesso.')
        else:
            messages.error(request, 'Não é possível cancelar esta reserva.')
        
        return redirect('bookings:list')


# ========================================
# NOVO FLUXO DE INSCRIÇÃO
# ========================================

class AdventureSelectionView(TemplateView):
    """
    Seleção de aventura - Página inicial do processo de inscrição
    """
    template_name = 'bookings/adventure_selection.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Buscar aventuras ativas e disponíveis
        context['adventures'] = Adventure.objects.filter(
            is_active=True,
            show_in_listing=True
        ).select_related('category').order_by('-is_featured', 'title')
        return context


class EventRegistrationStartView(TemplateView):
    """
    Página inicial do processo de inscrição - Verificação de CPF
    """
    template_name = 'bookings/registration_start.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        context['event'] = get_object_or_404(AdventureEvent, id=event_id)
        return context


class EventRegistrationDebugView(TemplateView):
    """
    Página de debug para verificação de CPF
    """
    template_name = 'bookings/registration_start_debug.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        context['event'] = get_object_or_404(AdventureEvent, id=event_id)
        return context


class CheckCPFView(TemplateView):
    """
    Verificação de CPF via AJAX
    """
    
    def post(self, request, *args, **kwargs):
        try:
            print(f"DEBUG: Recebido request body: {request.body}")
            data = json.loads(request.body)
            cpf = data.get('cpf', '').strip()
            event_id = self.kwargs.get('event_id')
            
            print(f"DEBUG: CPF recebido: '{cpf}', Event ID: {event_id}")
            
            if not cpf:
                print("DEBUG: CPF vazio")
                return JsonResponse({
                    'success': False,
                    'error': 'CPF é obrigatório'
                })
            
            # Limpar CPF
            clean_cpf = re.sub(r'[^0-9]', '', cpf)
            print(f"DEBUG: CPF limpo: '{clean_cpf}', tamanho: {len(clean_cpf)}")
            
            if len(clean_cpf) != 11:
                print("DEBUG: CPF com tamanho inválido")
                return JsonResponse({
                    'success': False,
                    'error': 'CPF deve conter 11 dígitos'
                })
            
            # Verificar se já existe usuário com este CPF
            existing_user = CustomUser.objects.filter(cpf=clean_cpf).first()
            print(f"DEBUG: Usuário encontrado: {existing_user}")
            
            if existing_user:
                # Cliente antigo - pode fazer inscrição direta
                redirect_url = f'/reservas/event/{event_id}/direct-registration/'
                print(f"DEBUG: Cliente existente, redirecionando para: {redirect_url}")
                return JsonResponse({
                    'success': True,
                    'is_existing_client': True,
                    'redirect_url': redirect_url
                })
            else:
                # Cliente novo - precisa fazer pré-inscrição
                redirect_url = f'/reservas/event/{event_id}/pre-registration/'
                print(f"DEBUG: Cliente novo, redirecionando para: {redirect_url}")
                return JsonResponse({
                    'success': True,
                    'is_existing_client': False,
                    'redirect_url': redirect_url
                })
                
        except Exception as e:
            print(f"DEBUG: Erro na view CheckCPFView: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': 'Erro interno. Tente novamente.'
            })


class PreRegistrationView(TemplateView):
    """
    Formulário de pré-inscrição para clientes novos
    """
    template_name = 'bookings/pre_registration.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        context['event'] = get_object_or_404(AdventureEvent, id=event_id)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            event_id = self.kwargs.get('event_id')
            event = get_object_or_404(AdventureEvent, id=event_id)
            
            # Validar dados
            required_fields = [
                'first_name', 'last_name', 'email', 'phone', 'cpf',
                'birth_date', 'emergency_contact_name', 'emergency_contact_phone',
                'address', 'city', 'state', 'zip_code'
            ]
            
            data = {}
            for field in required_fields:
                value = request.POST.get(field, '').strip()
                if not value:
                    messages.error(request, f'Campo {field} é obrigatório.')
                    return self.get(request, *args, **kwargs)
                data[field] = value
            
            # Limpar CPF
            data['cpf'] = re.sub(r'[^0-9]', '', data['cpf'])
            
            # Verificar se CPF já tem pré-inscrição para este evento
            if PreRegistration.objects.filter(cpf=data['cpf'], event=event).exists():
                messages.error(request, 'Já existe uma pré-inscrição com este CPF para este evento.')
                return self.get(request, *args, **kwargs)
            
            # Criar pré-inscrição
            pre_registration = PreRegistration.objects.create(
                **data,
                event=event,
                medical_conditions=request.POST.get('medical_conditions', ''),
                medications=request.POST.get('medications', ''),
                allergies=request.POST.get('allergies', ''),
                user_notes=request.POST.get('user_notes', ''),
                status='pending'
            )
            
            # Enviar mensagem WhatsApp
            WhatsAppService.send_pre_registration_message(pre_registration)
            
            messages.success(request, 'Pré-inscrição realizada com sucesso! Verifique seu WhatsApp.')
            return redirect('bookings:pre_registration_success', pre_registration_id=pre_registration.id)
            
        except Exception as e:
            messages.error(request, 'Erro ao processar pré-inscrição. Tente novamente.')
            return self.get(request, *args, **kwargs)


class PreRegistrationSuccessView(TemplateView):
    """
    Página de sucesso da pré-inscrição
    """
    template_name = 'bookings/pre_registration_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pre_registration_id = self.kwargs.get('pre_registration_id')
        context['pre_registration'] = get_object_or_404(
            PreRegistration, 
            id=pre_registration_id
        )
        return context


class DirectRegistrationView(TemplateView):
    """
    Inscrição direta para clientes antigos (com pagamento)
    """
    template_name = 'bookings/direct_registration.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        context['event'] = get_object_or_404(AdventureEvent, id=event_id)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            event_id = self.kwargs.get('event_id')
            event = get_object_or_404(AdventureEvent, id=event_id)
            
            cpf = request.POST.get('cpf', '').strip()
            cpf = re.sub(r'[^0-9]', '', cpf)
            
            # Encontrar usuário pelo CPF
            user = get_object_or_404(CustomUser, cpf=cpf)
            
            # Verificar se já tem reserva
            if Booking.objects.filter(user=user, event=event).exists():
                messages.error(request, 'Você já tem uma reserva para este evento.')
                return self.get(request, *args, **kwargs)
            
            # Criar reserva
            booking = Booking.objects.create(
                user=user,
                event=event,
                participants_count=1,
                total_price=event.final_price,
                status='pending',
                payment_status='pending'
            )
            
            return redirect('bookings:payment_options', booking_id=booking.id)
            
        except CustomUser.DoesNotExist:
            messages.error(request, 'CPF não encontrado.')
            return self.get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, 'Erro ao processar inscrição. Tente novamente.')
            return self.get(request, *args, **kwargs)


class PaymentOptionsView(TemplateView):
    """
    Página de opções de pagamento
    """
    template_name = 'bookings/payment_options.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.kwargs.get('booking_id')
        context['booking'] = get_object_or_404(Booking, id=booking_id)
        return context


class PIXPaymentView(TemplateView):
    """
    Página de pagamento via PIX
    """
    template_name = 'bookings/pix_payment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.kwargs.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Gerar PIX
        pix_payment = PIXService.generate_pix_payment(booking)
        
        context['booking'] = booking
        context['payment'] = pix_payment
        return context


class CreditCardPaymentView(TemplateView):
    """
    Página de pagamento via cartão de crédito
    """
    template_name = 'bookings/credit_card_payment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.kwargs.get('booking_id')
        context['booking'] = get_object_or_404(Booking, id=booking_id)
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            booking_id = self.kwargs.get('booking_id')
            booking = get_object_or_404(Booking, id=booking_id)
            
            # Dados do cartão
            card_data = {
                'number': request.POST.get('card_number', '').replace(' ', ''),
                'name': request.POST.get('card_name', ''),
                'expiry': request.POST.get('card_expiry', ''),
                'cvv': request.POST.get('card_cvv', ''),
            }
            
            installments = int(request.POST.get('installments', 1))
            
            # Processar pagamento
            payment = PaymentService.process_credit_card_payment(
                booking, card_data, installments
            )
            
            if payment and payment.status == 'approved':
                messages.success(request, 'Pagamento aprovado! Sua vaga está garantida.')
                return redirect('bookings:payment_success', booking_id=booking.id)
            else:
                messages.error(request, 'Pagamento rejeitado. Verifique os dados do cartão.')
                return self.get(request, *args, **kwargs)
                
        except Exception as e:
            messages.error(request, 'Erro ao processar pagamento. Tente novamente.')
            return self.get(request, *args, **kwargs)


class PaymentSuccessView(TemplateView):
    """
    Página de sucesso no pagamento
    """
    template_name = 'bookings/payment_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.kwargs.get('booking_id')
        context['booking'] = get_object_or_404(Booking, id=booking_id)
        return context


@method_decorator(csrf_exempt, name='dispatch')
class CheckPaymentStatusView(TemplateView):
    """
    Verificar status do pagamento (AJAX)
    """
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            payment_id = data.get('payment_id')
            
            payment = PaymentService.verify_pix_payment(payment_id)
            
            if payment:
                return JsonResponse({
                    'success': True,
                    'status': payment.status,
                    'is_approved': payment.status == 'approved'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Pagamento não encontrado'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'Erro ao verificar pagamento'
            })
