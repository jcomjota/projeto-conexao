import requests
import json
import qrcode
import io
import base64
from django.conf import settings
from django.utils import timezone
from .models import WhatsAppMessage, Payment
import logging

logger = logging.getLogger(__name__)


class WhatsAppService:
    """
    Serviço para envio de mensagens WhatsApp
    """
    COMPANY_PHONE = "5554993216261"  # Número da empresa
    
    @classmethod
    def send_message(cls, phone_number, message_text, message_type='custom', 
                     booking=None, pre_registration=None):
        """
        Envia mensagem via WhatsApp (usando WhatsApp Business API ou método alternativo)
        """
        try:
            # Limpar número de telefone
            clean_phone = cls._clean_phone_number(phone_number)
            
            # Criar log da mensagem
            whatsapp_message = WhatsAppMessage.objects.create(
                phone_number=clean_phone,
                recipient_name=cls._get_recipient_name(booking, pre_registration),
                message_type=message_type,
                message_text=message_text,
                booking=booking,
                pre_registration=pre_registration,
                status='pending'
            )
            
            # Para demonstração, vou usar o método de redirecionamento do WhatsApp Web
            # Em produção, você integraria com WhatsApp Business API
            success = cls._send_via_whatsapp_web(clean_phone, message_text)
            
            if success:
                whatsapp_message.status = 'sent'
                whatsapp_message.sent_at = timezone.now()
                whatsapp_message.save()
                logger.info(f"WhatsApp message sent to {clean_phone}")
            else:
                whatsapp_message.status = 'failed'
                whatsapp_message.save()
                logger.error(f"Failed to send WhatsApp message to {clean_phone}")
            
            return whatsapp_message
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            return None
    
    @classmethod
    def send_pre_registration_message(cls, pre_registration):
        """
        Envia mensagem de confirmação de pré-inscrição
        """
        message = f"""🌟 *Conexão Adventure* 🌟

Olá {pre_registration.get_full_name()}!

Sua pré-inscrição foi recebida com sucesso! ✅

*Aventura:* {pre_registration.event.adventure.title}
*Data:* {pre_registration.event.date.strftime('%d/%m/%Y')}
*Horário:* {pre_registration.event.start_time.strftime('%H:%M')}

🔄 *Próximos passos:*
Nossa equipe analisará sua inscrição e em breve entraremos em contato para confirmar sua vaga.

Aguarde nossa confirmação para prosseguir com o pagamento.

Dúvidas? Entre em contato: {cls.COMPANY_PHONE}

Obrigado pela preferência! 🚀"""
        
        return cls.send_message(
            pre_registration.phone,
            message,
            'pre_registration',
            pre_registration=pre_registration
        )
    
    @classmethod
    def send_payment_confirmation_message(cls, booking):
        """
        Envia mensagem de confirmação de pagamento
        """
        message = f"""🎉 *Pagamento Confirmado!* 🎉

Olá {booking.user.get_full_name()}!

Seu pagamento foi aprovado e sua vaga está garantida! ✅

*Aventura:* {booking.event.adventure.title}
*Data:* {booking.event.date.strftime('%d/%m/%Y')}
*Horário:* {booking.event.start_time.strftime('%H:%M')}
*Valor:* R$ {booking.total_price:.2f}

📍 *Informações importantes:*
- Chegue com 30 minutos de antecedência
- Traga documento com foto
- Use roupas adequadas para a atividade

Em breve enviaremos mais detalhes sobre a aventura.

Nos vemos em breve! 🚀

*Conexão Adventure*
WhatsApp: {cls.COMPANY_PHONE}"""
        
        return cls.send_message(
            booking.user.phone,
            message,
            'payment_confirmed',
            booking=booking
        )
    
    @classmethod
    def _clean_phone_number(cls, phone):
        """
        Limpa e formata número de telefone
        """
        # Remove caracteres não numéricos
        clean = ''.join(filter(str.isdigit, phone))
        
        # Adiciona código do país se necessário
        if len(clean) == 11 and clean.startswith('0'):
            clean = '55' + clean[1:]
        elif len(clean) == 10:
            clean = '5555' + clean
        elif len(clean) == 11 and not clean.startswith('55'):
            clean = '55' + clean
        
        return clean
    
    @classmethod
    def _get_recipient_name(cls, booking, pre_registration):
        """
        Obtém nome do destinatário
        """
        if booking:
            return booking.user.get_full_name()
        elif pre_registration:
            return pre_registration.get_full_name()
        return "Cliente"
    
    @classmethod
    def _send_via_whatsapp_web(cls, phone, message):
        """
        Simula envio via WhatsApp Web (para demonstração)
        Em produção, use WhatsApp Business API
        """
        try:
            # Esta é uma implementação para demonstração
            # Em produção, você usaria a API oficial do WhatsApp Business
            
            # Por enquanto, apenas retorna True para simular sucesso
            # O link pode ser usado para redirecionar o usuário
            whatsapp_url = f"https://wa.me/{phone}?text={requests.utils.quote(message)}"
            
            # Log da URL gerada
            logger.info(f"WhatsApp URL generated: {whatsapp_url}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in _send_via_whatsapp_web: {str(e)}")
            return False


class PIXService:
    """
    Serviço para geração de PIX
    """
    PIX_KEY = "54993216261"  # Chave PIX da empresa (telefone)
    
    @classmethod
    def generate_pix_payment(cls, booking, amount=None):
        """
        Gera pagamento PIX para uma reserva
        """
        try:
            payment_amount = amount or booking.total_price
            
            # Criar registro de pagamento
            payment = Payment.objects.create(
                booking=booking,
                payment_method='pix',
                amount=payment_amount,
                pix_key=cls.PIX_KEY,
                status='pending'
            )
            
            # Gerar dados do PIX
            pix_data = cls._generate_pix_data(payment)
            
            # Gerar QR Code
            qr_code = cls._generate_qr_code(pix_data)
            
            # Salvar dados no pagamento
            payment.pix_qr_code = qr_code
            payment.payment_data = {
                'pix_data': pix_data,
                'amount': float(payment_amount),
                'recipient': 'Conexão Adventure',
                'key': cls.PIX_KEY
            }
            payment.save()
            
            return payment
            
        except Exception as e:
            logger.error(f"Error generating PIX payment: {str(e)}")
            return None
    
    @classmethod
    def _generate_pix_data(cls, payment):
        """
        Gera dados do PIX (simulado)
        """
        # Esta é uma implementação simplificada
        # Em produção, você usaria uma biblioteca específica para PIX
        
        pix_data = {
            'key': cls.PIX_KEY,
            'amount': float(payment.amount),
            'description': f"Pagamento Aventura - Booking #{payment.booking.id}",
            'identifier': f"PAY{payment.id:06d}"
        }
        
        return json.dumps(pix_data)
    
    @classmethod
    def _generate_qr_code(cls, pix_data):
        """
        Gera QR Code para o PIX
        """
        try:
            # Criar QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(pix_data)
            qr.make(fit=True)
            
            # Criar imagem
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Converter para base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            logger.error(f"Error generating QR code: {str(e)}")
            return ""


class PaymentService:
    """
    Serviço para processamento de pagamentos
    """
    
    @classmethod
    def process_credit_card_payment(cls, booking, card_data, installments=1):
        """
        Processa pagamento com cartão de crédito
        """
        try:
            # Criar registro de pagamento
            payment = Payment.objects.create(
                booking=booking,
                payment_method='credit_card',
                amount=booking.total_price,
                installments=installments,
                status='processing'
            )
            
            # Simular processamento do cartão
            # Em produção, você integraria com Mercado Pago, Stripe, etc.
            success = cls._process_card_payment(payment, card_data)
            
            if success:
                payment.status = 'approved'
                payment.processed_at = timezone.now()
                payment.save()
                
                # Atualizar status da reserva
                booking.payment_status = 'paid'
                booking.status = 'approved'
                booking.save()
                
                # Enviar mensagem de confirmação
                WhatsAppService.send_payment_confirmation_message(booking)
                
                logger.info(f"Credit card payment approved for booking {booking.id}")
            else:
                payment.status = 'rejected'
                payment.save()
                logger.error(f"Credit card payment rejected for booking {booking.id}")
            
            return payment
            
        except Exception as e:
            logger.error(f"Error processing credit card payment: {str(e)}")
            return None
    
    @classmethod
    def _process_card_payment(cls, payment, card_data):
        """
        Simula processamento do cartão (para demonstração)
        """
        # Esta é uma implementação para demonstração
        # Em produção, você integraria com um gateway de pagamento real
        
        # Simular verificações básicas
        if not card_data.get('number') or not card_data.get('cvv'):
            return False
        
        # Simular aprovação (90% de aprovação para demonstração)
        import random
        return random.random() > 0.1
    
    @classmethod
    def verify_pix_payment(cls, payment_id):
        """
        Verifica status do pagamento PIX
        """
        try:
            payment = Payment.objects.get(id=payment_id)
            
            # Em produção, você consultaria a API do banco
            # Para demonstração, vamos simular
            
            # Simular confirmação após algum tempo
            if payment.status == 'pending':
                # Simular que alguns pagamentos são confirmados
                import random
                if random.random() > 0.7:  # 30% de chance de confirmação
                    payment.status = 'approved'
                    payment.processed_at = timezone.now()
                    payment.save()
                    
                    # Atualizar reserva
                    booking = payment.booking
                    booking.payment_status = 'paid'
                    booking.status = 'approved'
                    booking.save()
                    
                    # Enviar confirmação
                    WhatsAppService.send_payment_confirmation_message(booking)
            
            return payment
            
        except Payment.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error verifying PIX payment: {str(e)}")
            return None 