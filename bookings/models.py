from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.urls import reverse


User = get_user_model()


class AdventureEvent(models.Model):
    """
    Eventos específicos de uma aventura (datas agendadas)
    """
    STATUS_CHOICES = [
        ('scheduled', 'Agendado'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado'),
        ('completed', 'Concluído'),
    ]
    
    adventure = models.ForeignKey(
        'adventures.Adventure', 
        on_delete=models.CASCADE, 
        related_name='events',
        verbose_name="Aventura"
    )
    
    # Data e horário
    date = models.DateField(verbose_name="Data")
    start_time = models.TimeField(verbose_name="Horário de Início")
    end_time = models.TimeField(
        null=True, 
        blank=True, 
        verbose_name="Horário de Término"
    )
    
    # Configurações específicas do evento
    max_participants = models.PositiveIntegerField(
        verbose_name="Máximo de Participantes"
    )
    current_participants = models.PositiveIntegerField(
        default=0,
        verbose_name="Participantes Atuais"
    )
    
    # Preço específico para este evento (opcional)
    custom_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Preço Personalizado",
        help_text="Deixe em branco para usar o preço da aventura"
    )
    
    # Status e configurações
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='scheduled',
        verbose_name="Status"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    registration_deadline = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Prazo para Inscrições"
    )
    
    # Informações específicas
    meeting_instructions = models.TextField(
        blank=True,
        verbose_name="Instruções de Encontro",
        help_text="Instruções específicas para este evento"
    )
    special_notes = models.TextField(
        blank=True,
        verbose_name="Observações Especiais"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_events',
        verbose_name="Criado por"
    )
    
    class Meta:
        verbose_name = "Evento de Aventura"
        verbose_name_plural = "Eventos de Aventuras"
        ordering = ['date', 'start_time']
        unique_together = ['adventure', 'date', 'start_time']
    
    def __str__(self):
        return f"{self.adventure.title} - {self.date.strftime('%d/%m/%Y')}"
    
    @property
    def is_full(self):
        """Verifica se o evento está lotado"""
        return self.current_participants >= self.max_participants
    
    @property
    def available_spots(self):
        """Retorna vagas disponíveis"""
        return self.max_participants - self.current_participants
    
    @property
    def registration_open(self):
        """Verifica se as inscrições estão abertas"""
        if not self.is_active or self.status != 'scheduled':
            return False
        
        if self.registration_deadline:
            return timezone.now() <= self.registration_deadline
        
        # Se não há deadline, permite até o dia do evento
        return timezone.now().date() <= self.date
    
    @property
    def final_price(self):
        """Retorna o preço final do evento"""
        if self.custom_price:
            return self.custom_price
        return self.adventure.current_price


class Booking(models.Model):
    """
    Modelo principal para inscrições nas aventuras
    """
    STATUS_CHOICES = [
        ('pending', 'Aguardando Aprovação'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('cancelled', 'Cancelado'),
        ('completed', 'Concluído'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('partial', 'Parcial'),
        ('paid', 'Pago'),
        ('refunded', 'Reembolsado'),
    ]
    
    # Relacionamentos principais
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name="Usuário"
    )
    event = models.ForeignKey(
        AdventureEvent, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name="Evento"
    )
    
    # Informações da reserva
    participants_count = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Número de Participantes"
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Preço Total"
    )
    
    # Status
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Status da Reserva"
    )
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending',
        verbose_name="Status do Pagamento"
    )
    
    # Observações
    user_notes = models.TextField(
        blank=True,
        verbose_name="Observações do Usuário",
        help_text="Comentários ou solicitações especiais"
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name="Observações da Administração",
        help_text="Notas internas para a equipe"
    )
    
    # Informações de contato específicas
    contact_phone = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name="Telefone de Contato"
    )
    emergency_contact = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Contato de Emergência"
    )
    emergency_phone = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name="Telefone de Emergência"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Aprovado em"
    )
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_bookings',
        verbose_name="Aprovado por"
    )
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-created_at']
        unique_together = ['user', 'event']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.event}"
    
    def save(self, *args, **kwargs):
        # Calcular preço total se não foi definido
        if not self.total_price:
            self.total_price = self.event.final_price * self.participants_count
        super().save(*args, **kwargs)
        
        # Atualizar contagem de participantes do evento
        self.event.current_participants = self.event.bookings.filter(
            status='approved'
        ).aggregate(
            total=models.Sum('participants_count')
        )['total'] or 0
        self.event.save(update_fields=['current_participants'])
    
    def get_absolute_url(self):
        return reverse('booking_detail', kwargs={'pk': self.pk})
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @property
    def can_cancel(self):
        """Verifica se a reserva pode ser cancelada"""
        if self.status in ['cancelled', 'completed']:
            return False
        
        # Permite cancelamento até 24h antes do evento
        event_datetime = timezone.datetime.combine(
            self.event.date, 
            self.event.start_time
        )
        event_datetime = timezone.make_aware(event_datetime)
        
        return timezone.now() < (event_datetime - timezone.timedelta(hours=24))


class AdventureChecklist(models.Model):
    """
    Checklist específico para cada aventura
    """
    ITEM_TYPE_CHOICES = [
        ('equipment', 'Equipamento'),
        ('clothing', 'Vestuário'),
        ('food', 'Alimentação'),
        ('document', 'Documento'),
        ('personal', 'Item Pessoal'),
        ('medical', 'Médico/Saúde'),
    ]
    
    adventure = models.ForeignKey(
        'adventures.Adventure', 
        on_delete=models.CASCADE, 
        related_name='checklist_items',
        verbose_name="Aventura"
    )
    
    item_name = models.CharField(max_length=200, verbose_name="Item")
    item_type = models.CharField(
        max_length=20, 
        choices=ITEM_TYPE_CHOICES,
        verbose_name="Tipo de Item"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descrição",
        help_text="Detalhes ou especificações do item"
    )
    
    is_required = models.BooleanField(
        default=True, 
        verbose_name="Obrigatório"
    )
    is_provided = models.BooleanField(
        default=False, 
        verbose_name="Fornecido pela empresa"
    )
    
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Ordem"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Item do Checklist"
        verbose_name_plural = "Itens do Checklist"
        ordering = ['adventure', 'item_type', 'order', 'item_name']
    
    def __str__(self):
        status = "Obrigatório" if self.is_required else "Opcional"
        provided = " (Fornecido)" if self.is_provided else ""
        return f"{self.item_name} - {status}{provided}"


class UserChecklist(models.Model):
    """
    Checklist do usuário para uma reserva específica
    """
    booking = models.ForeignKey(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='user_checklist',
        verbose_name="Reserva"
    )
    checklist_item = models.ForeignKey(
        AdventureChecklist, 
        on_delete=models.CASCADE,
        verbose_name="Item do Checklist"
    )
    
    is_checked = models.BooleanField(
        default=False, 
        verbose_name="Marcado"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Observações",
        help_text="Observações pessoais sobre este item"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Checklist do Usuário"
        verbose_name_plural = "Checklists dos Usuários"
        unique_together = ['booking', 'checklist_item']
        ordering = ['checklist_item__order', 'checklist_item__item_name']
    
    def __str__(self):
        status = "✓" if self.is_checked else "○"
        return f"{status} {self.checklist_item.item_name}"


class InsuranceInfo(models.Model):
    """
    Informações de seguro para aventuras
    """
    adventure = models.OneToOneField(
        'adventures.Adventure', 
        on_delete=models.CASCADE, 
        related_name='insurance_info',
        verbose_name="Aventura"
    )
    
    insurance_company = models.CharField(
        max_length=200,
        verbose_name="Seguradora"
    )
    policy_number = models.CharField(
        max_length=100,
        verbose_name="Número da Apólice"
    )
    coverage_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Valor da Cobertura"
    )
    
    coverage_details = models.TextField(
        verbose_name="Detalhes da Cobertura"
    )
    exclusions = models.TextField(
        blank=True,
        verbose_name="Exclusões"
    )
    
    contact_phone = models.CharField(
        max_length=20,
        verbose_name="Telefone da Seguradora"
    )
    emergency_contact = models.CharField(
        max_length=20,
        verbose_name="Contato de Emergência"
    )
    
    valid_from = models.DateField(verbose_name="Válido de")
    valid_until = models.DateField(verbose_name="Válido até")
    
    additional_info = models.TextField(
        blank=True,
        verbose_name="Informações Adicionais"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Informação de Seguro"
        verbose_name_plural = "Informações de Seguro"
    
    def __str__(self):
        return f"Seguro - {self.adventure.title}"
    
    @property
    def is_valid(self):
        """Verifica se o seguro está válido"""
        today = timezone.now().date()
        return self.valid_from <= today <= self.valid_until


class EventDocument(models.Model):
    """
    Documentos específicos para eventos (termos, declarações, etc.)
    """
    DOCUMENT_TYPE_CHOICES = [
        ('waiver', 'Termo de Responsabilidade'),
        ('insurance', 'Documento de Seguro'),
        ('checklist', 'Checklist'),
        ('instructions', 'Instruções'),
        ('map', 'Mapa/Localização'),
        ('other', 'Outro'),
    ]
    
    event = models.ForeignKey(
        AdventureEvent, 
        on_delete=models.CASCADE, 
        related_name='documents',
        verbose_name="Evento"
    )
    
    title = models.CharField(max_length=200, verbose_name="Título")
    document_type = models.CharField(
        max_length=20, 
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name="Tipo de Documento"
    )
    
    file = models.FileField(
        upload_to='event_documents/',
        verbose_name="Arquivo"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    
    is_required_reading = models.BooleanField(
        default=False,
        verbose_name="Leitura Obrigatória"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Documento do Evento"
        verbose_name_plural = "Documentos dos Eventos"
        ordering = ['-is_required_reading', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.event}"


class Payment(models.Model):
    """
    Modelo para controlar pagamentos das inscrições
    """
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Cartão de Crédito'),
        ('pix', 'PIX'),
        ('bank_transfer', 'Transferência Bancária'),
        ('cash', 'Dinheiro'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('refunded', 'Reembolsado'),
        ('cancelled', 'Cancelado'),
    ]
    
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Reserva"
    )
    
    # Informações do pagamento
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Método de Pagamento"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor"
    )
    installments = models.PositiveIntegerField(
        default=1,
        verbose_name="Parcelas"
    )
    
    # Status e identificadores
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name="Status"
    )
    external_payment_id = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="ID do Pagamento Externo"
    )
    
    # PIX específico
    pix_key = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Chave PIX"
    )
    pix_qr_code = models.TextField(
        blank=True,
        verbose_name="QR Code PIX"
    )
    
    # Informações extras
    payment_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Dados do Pagamento"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Processado em"
    )
    
    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pagamento {self.id} - {self.booking.user.get_full_name()} - R$ {self.amount}"


class PreRegistration(models.Model):
    """
    Pré-inscrições para clientes novos
    """
    STATUS_CHOICES = [
        ('pending', 'Aguardando Análise'),
        ('approved', 'Aprovado - Pode Pagar'),
        ('rejected', 'Rejeitado'),
        ('converted', 'Convertido em Inscrição'),
    ]
    
    # Informações pessoais
    first_name = models.CharField(max_length=50, verbose_name="Nome")
    last_name = models.CharField(max_length=50, verbose_name="Sobrenome")
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    cpf = models.CharField(max_length=14, verbose_name="CPF")
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    
    # Contato de emergência
    emergency_contact_name = models.CharField(
        max_length=100,
        verbose_name="Nome do Contato de Emergência"
    )
    emergency_contact_phone = models.CharField(
        max_length=20,
        verbose_name="Telefone do Contato de Emergência"
    )
    
    # Endereço
    address = models.TextField(verbose_name="Endereço")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado")
    zip_code = models.CharField(max_length=10, verbose_name="CEP")
    
    # Informações médicas
    medical_conditions = models.TextField(
        blank=True,
        verbose_name="Condições Médicas"
    )
    medications = models.TextField(
        blank=True,
        verbose_name="Medicamentos"
    )
    allergies = models.TextField(
        blank=True,
        verbose_name="Alergias"
    )
    
    # Evento
    event = models.ForeignKey(
        AdventureEvent,
        on_delete=models.CASCADE,
        related_name='pre_registrations',
        verbose_name="Evento"
    )
    
    # Status e observações
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Status"
    )
    user_notes = models.TextField(
        blank=True,
        verbose_name="Observações do Cliente"
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name="Observações da Administração"
    )
    
    # Usuário criado (quando convertido)
    created_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pre_registrations',
        verbose_name="Usuário Criado"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Aprovado em"
    )
    
    class Meta:
        verbose_name = "Pré-inscrição"
        verbose_name_plural = "Pré-inscrições"
        ordering = ['-created_at']
        unique_together = ['cpf', 'event']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class WhatsAppMessage(models.Model):
    """
    Log de mensagens WhatsApp enviadas
    """
    MESSAGE_TYPE_CHOICES = [
        ('pre_registration', 'Pré-inscrição'),
        ('registration_confirmed', 'Inscrição Confirmada'),
        ('payment_confirmed', 'Pagamento Confirmado'),
        ('event_reminder', 'Lembrete do Evento'),
        ('cancellation', 'Cancelamento'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('sent', 'Enviado'),
        ('delivered', 'Entregue'),
        ('read', 'Lido'),
        ('failed', 'Falhou'),
    ]
    
    # Destinatário
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Número do Telefone"
    )
    recipient_name = models.CharField(
        max_length=200,
        verbose_name="Nome do Destinatário"
    )
    
    # Mensagem
    message_type = models.CharField(
        max_length=30,
        choices=MESSAGE_TYPE_CHOICES,
        verbose_name="Tipo da Mensagem"
    )
    message_text = models.TextField(verbose_name="Texto da Mensagem")
    
    # Relacionamentos (opcional)
    booking = models.ForeignKey(
        Booking,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='whatsapp_messages',
        verbose_name="Reserva"
    )
    pre_registration = models.ForeignKey(
        PreRegistration,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='whatsapp_messages',
        verbose_name="Pré-inscrição"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Status"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Enviado em"
    )
    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Entregue em"
    )
    
    class Meta:
        verbose_name = "Mensagem WhatsApp"
        verbose_name_plural = "Mensagens WhatsApp"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.message_type} para {self.recipient_name} - {self.status}"
