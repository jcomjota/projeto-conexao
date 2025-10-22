from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    AdventureEvent, Booking, AdventureChecklist, UserChecklist,
    InsuranceInfo, EventDocument, Payment, PreRegistration, WhatsAppMessage
)
from users.models import CustomUser
import random
import string
from services.whatsapp import WhatsAppService


@admin.register(AdventureEvent)
class AdventureEventAdmin(admin.ModelAdmin):
    list_display = [
        'adventure', 'date', 'start_time', 'status', 
        'current_participants', 'max_participants', 'available_spots_display'
    ]
    list_filter = ['status', 'date', 'adventure']
    search_fields = ['adventure__title', 'adventure__slug']
    ordering = ['-date', '-start_time']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('adventure', 'date', 'start_time', 'end_time')
        }),
        ('Configurações', {
            'fields': ('max_participants', 'current_participants', 'custom_price', 'status', 'is_active')
        }),
        ('Configurações Avançadas', {
            'fields': ('registration_deadline', 'meeting_instructions', 'special_notes'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def available_spots_display(self, obj):
        spots = obj.available_spots
        if spots <= 0:
            color = 'red'
            icon = '❌'
        elif spots <= 3:
            color = 'orange'
            icon = '⚠️'
        else:
            color = 'green'
            icon = '✅'
        
        return format_html(
            '<span style="color: {};">{} {} vagas</span>',
            color, icon, spots
        )
    available_spots_display.short_description = 'Vagas Disponíveis'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']


@admin.register(PreRegistration)
class PreRegistrationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'cpf', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'cpf']
    actions = ['convert_to_user']

    def convert_to_user(self, request, queryset):
        converted_count = 0
        for pre_reg in queryset:
            # Verificar se já existe um usuário com este CPF
            existing_user = CustomUser.objects.filter(cpf=pre_reg.cpf).first()
            if existing_user:
                pre_reg.created_user = existing_user
                pre_reg.status = 'converted'
                pre_reg.save()
                converted_count += 1
                continue
            
            # Se não existe usuário, criar um novo
            username = f"{pre_reg.first_name.lower()}.{pre_reg.last_name.lower()}.{random.randint(1000, 9999)}"
            password = "Aventura@2024"  # Senha padrão
            
            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    email=pre_reg.email,
                    first_name=pre_reg.first_name,
                    last_name=pre_reg.last_name,
                    password=password,
                    phone=pre_reg.phone,
                    cpf=pre_reg.cpf
                )
                
                # Atualizar pré-registro
                pre_reg.created_user = user
                pre_reg.status = 'converted'
                pre_reg.save()
                
                # Enviar credenciais por WhatsApp
                message = f"Bem-vindo à Conexão Adventure! Suas credenciais de acesso:\nEmail: {pre_reg.email}\nSenha: {password}\n\nRecomendamos que você altere sua senha no primeiro acesso."
                WhatsAppService.send_message(pre_reg.phone, message)
                
                converted_count += 1
            except Exception as e:
                self.message_user(request, f"Erro ao converter {pre_reg.email}: {str(e)}", level=messages.ERROR)
        
        if converted_count > 0:
            self.message_user(request, f"{converted_count} pré-inscrições foram convertidas em usuários.")
        else:
            self.message_user(request, "Nenhuma pré-inscrição foi convertida em usuário.", level=messages.WARNING)
    convert_to_user.short_description = "Converter em usuários (aprovadas)"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'booking', 'payment_method', 'amount', 
        'status', 'installments', 'created_at'
    ]
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['booking__user__email', 'external_payment_id']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'processed_at']
    
    fieldsets = (
        ('Informações do Pagamento', {
            'fields': ('booking', 'payment_method', 'amount', 'installments')
        }),
        ('Status', {
            'fields': ('status', 'external_payment_id')
        }),
        ('PIX (se aplicável)', {
            'fields': ('pix_key', 'pix_qr_code'),
            'classes': ('collapse',)
        }),
        ('Dados Adicionais', {
            'fields': ('payment_data',),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at', 'processed_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['approve_payments', 'reject_payments']
    
    def approve_payments(self, request, queryset):
        from django.utils import timezone
        count = 0
        for payment in queryset.filter(status__in=['pending', 'processing']):
            payment.status = 'approved'
            payment.processed_at = timezone.now()
            payment.save()
            
            # Atualizar booking
            booking = payment.booking
            booking.payment_status = 'paid'
            booking.status = 'approved'
            booking.save()
            
            count += 1
        
        self.message_user(request, f'{count} pagamentos foram aprovados.')
    approve_payments.short_description = 'Aprovar pagamentos selecionados'
    
    def reject_payments(self, request, queryset):
        count = queryset.filter(status__in=['pending', 'processing']).update(status='rejected')
        self.message_user(request, f'{count} pagamentos foram rejeitados.')
    reject_payments.short_description = 'Rejeitar pagamentos selecionados'


@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'recipient_name', 'phone_number', 'message_type', 
        'status', 'created_at', 'sent_at'
    ]
    list_filter = ['message_type', 'status', 'created_at']
    search_fields = ['recipient_name', 'phone_number']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'sent_at', 'delivered_at']
    
    fieldsets = (
        ('Destinatário', {
            'fields': ('recipient_name', 'phone_number')
        }),
        ('Mensagem', {
            'fields': ('message_type', 'message_text')
        }),
        ('Relacionamentos', {
            'fields': ('booking', 'pre_registration'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'sent_at', 'delivered_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(AdventureChecklist)
class AdventureChecklistAdmin(admin.ModelAdmin):
    list_display = ['adventure', 'item_name', 'item_type', 'is_required', 'is_provided', 'order']
    list_filter = ['item_type', 'is_required', 'is_provided', 'adventure']
    search_fields = ['item_name', 'adventure__title']
    ordering = ['adventure', 'item_type', 'order']


@admin.register(UserChecklist)
class UserChecklistAdmin(admin.ModelAdmin):
    list_display = ['booking', 'checklist_item', 'is_checked']
    list_filter = ['is_checked', 'checklist_item__item_type']
    search_fields = ['booking__user__email', 'checklist_item__item_name']


@admin.register(InsuranceInfo)
class InsuranceInfoAdmin(admin.ModelAdmin):
    list_display = ['adventure', 'insurance_company', 'policy_number', 'valid_from', 'valid_until']
    list_filter = ['insurance_company', 'valid_from', 'valid_until']
    search_fields = ['adventure__title', 'insurance_company', 'policy_number']


@admin.register(EventDocument)
class EventDocumentAdmin(admin.ModelAdmin):
    list_display = ['event', 'title', 'document_type', 'is_required_reading']
    list_filter = ['document_type', 'is_required_reading', 'event__adventure']
    search_fields = ['title', 'event__adventure__title']
