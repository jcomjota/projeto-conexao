from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class Badge(models.Model):
    """
    Modelo para insígnias que os usuários podem conquistar
    """
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    icon = models.CharField(max_length=50, verbose_name="Ícone")
    points = models.PositiveIntegerField(default=0, verbose_name="Pontos")
    requirement_type = models.CharField(
        max_length=50,
        choices=[
            ('adventures_completed', 'Aventuras Completadas'),
            ('points_earned', 'Pontos Acumulados'),
            ('specific_adventure', 'Aventura Específica'),
            ('payment_method', 'Método de Pagamento'),
        ],
        verbose_name="Tipo de Requisito"
    )
    requirement_value = models.JSONField(
        default=dict,
        verbose_name="Valor do Requisito",
        help_text="Configuração específica do requisito em formato JSON"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Insígnia"
        verbose_name_plural = "Insígnias"

    def __str__(self):
        return self.name


class Reward(models.Model):
    """
    Modelo para recompensas que podem ser resgatadas com pontos
    """
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    icon = models.CharField(max_length=50, verbose_name="Ícone")
    points_cost = models.PositiveIntegerField(verbose_name="Custo em Pontos")
    reward_type = models.CharField(
        max_length=50,
        choices=[
            ('discount', 'Desconto'),
            ('free_adventure', 'Aventura Grátis'),
            ('merchandise', 'Brinde'),
        ],
        verbose_name="Tipo de Recompensa"
    )
    value = models.JSONField(
        default=dict,
        verbose_name="Valor da Recompensa",
        help_text="Configuração específica da recompensa em formato JSON"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recompensa"
        verbose_name_plural = "Recompensas"

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """
    Modelo para registrar as insígnias conquistadas pelos usuários
    """
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')
        verbose_name = "Insígnia do Usuário"
        verbose_name_plural = "Insígnias dos Usuários"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.badge.name}"


class UserReward(models.Model):
    """
    Modelo para registrar as recompensas resgatadas pelos usuários
    """
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='user_rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pendente'),
            ('approved', 'Aprovado'),
            ('used', 'Utilizado'),
            ('expired', 'Expirado'),
        ],
        default='pending'
    )
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Recompensa do Usuário"
        verbose_name_plural = "Recompensas dos Usuários"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.reward.name}"


class CustomUser(AbstractUser):
    """
    Modelo de usuário customizado para aventureiros
    """
    email = models.EmailField(unique=True, verbose_name="E-mail")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Número de telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        verbose_name="Telefone"
    )
    is_guide = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    
    # Resolvendo conflito de related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    cpf = models.CharField(max_length=14, blank=True, verbose_name="CPF")
    emergency_contact_name = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Nome do Contato de Emergência"
    )
    emergency_contact_phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        verbose_name="Telefone do Contato de Emergência"
    )
    address = models.TextField(blank=True, verbose_name="Endereço")
    city = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=2, blank=True, verbose_name="Estado")
    zip_code = models.CharField(max_length=10, blank=True, verbose_name="CEP")
    
    # Configurações de preferências
    receive_notifications = models.BooleanField(
        default=True, 
        verbose_name="Receber notificações por e-mail"
    )
    newsletter_subscription = models.BooleanField(
        default=False, 
        verbose_name="Assinatura da newsletter"
    )
    
    # Informações de aventuras e gamificação
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('iniciante', 'Iniciante'),
            ('intermediario', 'Intermediário'),
            ('avancado', 'Avançado'),
            ('expert', 'Expert'),
        ],
        default='iniciante',
        verbose_name="Nível de Experiência"
    )
    
    adventurer_level = models.CharField(
        max_length=50,
        choices=[
            ('iniciante_trilha', 'Iniciante de Trilha'),
            ('explorador_selva', 'Explorador de Selva'),
            ('guerreiro_alturas', 'Guerreiro das Alturas'),
            ('mestre_aventuras', 'Mestre das Aventuras'),
        ],
        default='iniciante_trilha',
        verbose_name="Nível do Aventureiro"
    )
    
    total_points = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de Pontos"
    )
    
    available_points = models.PositiveIntegerField(
        default=0,
        verbose_name="Pontos Disponíveis"
    )
    
    level_progress = models.PositiveIntegerField(
        default=0,
        verbose_name="Progresso do Nível",
        help_text="Porcentagem de progresso para o próximo nível (0-100)"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Retorna nome completo do usuário"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def total_adventures(self):
        """Retorna total de aventuras do usuário"""
        return self.bookings.filter(status='approved').count()
    
    @property
    def completed_adventures_count(self):
        """Retorna o número de aventuras completadas"""
        return self.bookings.filter(status='completed').count()
    
    @property
    def badges(self):
        """Retorna todas as insígnias do usuário"""
        return Badge.objects.filter(userbadge__user=self)
    
    def add_points(self, points, adventure=None):
        """Adiciona pontos ao usuário e atualiza seu progresso"""
        self.total_points += points
        self.available_points += points
        
        # Atualiza o nível do aventureiro com base nos pontos
        if self.total_points >= 1000:
            self.adventurer_level = 'mestre_aventuras'
            self.level_progress = 100
        elif self.total_points >= 500:
            self.adventurer_level = 'guerreiro_alturas'
            self.level_progress = ((self.total_points - 500) / 500) * 100
        elif self.total_points >= 200:
            self.adventurer_level = 'explorador_selva'
            self.level_progress = ((self.total_points - 200) / 300) * 100
        else:
            self.level_progress = (self.total_points / 200) * 100
        
        self.save()
        
        # Verifica e concede insígnias
        self.check_and_award_badges(adventure)
    
    def check_and_award_badges(self, adventure=None):
        """Verifica e concede insígnias baseado nas conquistas do usuário"""
        for badge in Badge.objects.all():
            # Pula se já tem a insígnia
            if UserBadge.objects.filter(user=self, badge=badge).exists():
                continue
            
            awarded = False
            if badge.requirement_type == 'adventures_completed':
                if self.completed_adventures_count >= badge.requirement_value.get('count', 0):
                    awarded = True
            elif badge.requirement_type == 'points_earned':
                if self.total_points >= badge.requirement_value.get('points', 0):
                    awarded = True
            elif badge.requirement_type == 'specific_adventure' and adventure:
                if str(adventure.id) == str(badge.requirement_value.get('adventure_id')):
                    awarded = True
            elif badge.requirement_type == 'payment_method' and adventure:
                if adventure.payment_method == badge.requirement_value.get('method'):
                    awarded = True
            
            if awarded:
                UserBadge.objects.create(user=self, badge=badge)
                self.add_points(badge.points)  # Pontos bônus da insígnia
    
    def redeem_reward(self, reward):
        """Resgata uma recompensa usando pontos disponíveis"""
        if self.available_points >= reward.points_cost and reward.is_active:
            self.available_points -= reward.points_cost
            self.save()
            return UserReward.objects.create(user=self, reward=reward)
        return None


class UserProfile(models.Model):
    """
    Perfil adicional do usuário com informações extras
    """
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name="Usuário"
    )
    bio = models.TextField(blank=True, verbose_name="Biografia")
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True, 
        verbose_name="Foto do Perfil"
    )
    
    # Informações médicas/saúde
    medical_conditions = models.TextField(
        blank=True, 
        verbose_name="Condições Médicas",
        help_text="Informe qualquer condição médica relevante para as atividades"
    )
    medications = models.TextField(
        blank=True, 
        verbose_name="Medicamentos",
        help_text="Liste medicamentos em uso regular"
    )
    allergies = models.TextField(
        blank=True, 
        verbose_name="Alergias",
        help_text="Informe alergias conhecidas"
    )
    
    # Preferências
    preferred_activities = models.JSONField(
        default=list, 
        blank=True,
        verbose_name="Atividades Preferidas"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"
