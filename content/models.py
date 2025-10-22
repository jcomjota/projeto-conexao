from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField


class Banner(models.Model):
    """
    Modelo para banners da home page (fotos e vídeos)
    """
    MEDIA_TYPE_CHOICES = [
        ('image', 'Imagem'),
        ('video', 'Vídeo'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    subtitle = models.CharField(
        max_length=300, 
        blank=True, 
        verbose_name="Subtítulo"
    )
    media_type = models.CharField(
        max_length=10, 
        choices=MEDIA_TYPE_CHOICES, 
        default='image',
        verbose_name="Tipo de Mídia"
    )
    
    # Para imagens
    image = models.ImageField(
        upload_to='banners/images/', 
        blank=True, 
        null=True,
        verbose_name="Imagem"
    )
    
    # Para vídeos
    video = models.FileField(
        upload_to='banners/videos/', 
        blank=True, 
        null=True,
        verbose_name="Vídeo",
        help_text="Formatos suportados: MP4, WEBM"
    )
    
    # Configurações de exibição
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Ordem de Exibição"
    )
    
    # Botões de ação (opcional)
    primary_button_text = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="Texto Botão Principal"
    )
    primary_button_url = models.URLField(
        blank=True, 
        verbose_name="URL Botão Principal"
    )
    secondary_button_text = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="Texto Botão Secundário"
    )
    secondary_button_url = models.URLField(
        blank=True, 
        verbose_name="URL Botão Secundário"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.media_type == 'image' and not self.image:
            raise ValidationError('Imagem é obrigatória quando o tipo é "Imagem"')
        if self.media_type == 'video' and not self.video:
            raise ValidationError('Vídeo é obrigatório quando o tipo é "Vídeo"')


class Testimonial(models.Model):
    """
    Modelo para depoimentos (incluindo integração com TripAdvisor)
    """
    SOURCE_CHOICES = [
        ('manual', 'Manual'),
        ('tripadvisor', 'TripAdvisor'),
        ('google', 'Google Reviews'),
        ('facebook', 'Facebook'),
    ]
    
    author_name = models.CharField(max_length=100, verbose_name="Nome do Autor")
    author_city = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Cidade do Autor"
    )
    author_avatar = models.ImageField(
        upload_to='testimonials/avatars/', 
        blank=True, 
        null=True,
        verbose_name="Foto do Autor"
    )
    
    content = models.TextField(verbose_name="Conteúdo do Depoimento")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        verbose_name="Avaliação (1-5 estrelas)"
    )
    
    # Data da aventura/experiência
    adventure_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Data da Aventura"
    )
    adventure_title = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name="Título da Aventura"
    )
    
    # Configurações de origem
    source = models.CharField(
        max_length=20, 
        choices=SOURCE_CHOICES, 
        default='manual',
        verbose_name="Origem"
    )
    external_id = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="ID Externo",
        help_text="ID do depoimento na plataforma externa"
    )
    external_url = models.URLField(
        blank=True,
        verbose_name="URL Externa",
        help_text="Link para o depoimento original"
    )
    
    # Configurações de exibição
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_featured = models.BooleanField(
        default=False, 
        verbose_name="Destacar"
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Ordem de Exibição"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Depoimento"
        verbose_name_plural = "Depoimentos"
        ordering = ['-is_featured', 'order', '-created_at']
    
    def __str__(self):
        return f"{self.author_name} - {self.rating}⭐"
    
    @property
    def stars_display(self):
        """Retorna string com estrelas para exibição"""
        return "⭐" * self.rating


class StatisticCounter(models.Model):
    """
    Contadores estatísticos para a home page
    """
    name = models.CharField(max_length=100, verbose_name="Nome")
    value = models.PositiveIntegerField(verbose_name="Valor")
    suffix = models.CharField(
        max_length=10, 
        blank=True,
        verbose_name="Sufixo",
        help_text="Ex: +, k+, %, etc."
    )
    icon = models.CharField(
        max_length=50, 
        blank=True,
        verbose_name="Ícone",
        help_text="Classe CSS do ícone FontAwesome"
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Ordem de Exibição"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contador Estatístico"
        verbose_name_plural = "Contadores Estatísticos"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name}: {self.value}{self.suffix}"


class EditablePage(models.Model):
    """
    Páginas editáveis como "Como Funciona" e "Regras Gerais"
    """
    PAGE_CHOICES = [
        ('como_funciona', 'Como Funciona'),
        ('regras_gerais', 'Regras Gerais'),
        ('sobre', 'Sobre Nós'),
        ('termos', 'Termos e Condições'),
        ('privacidade', 'Política de Privacidade'),
    ]
    
    page_type = models.CharField(
        max_length=20, 
        choices=PAGE_CHOICES, 
        unique=True,
        verbose_name="Tipo de Página"
    )
    title = models.CharField(max_length=200, verbose_name="Título")
    subtitle = models.CharField(
        max_length=300, 
        blank=True, 
        verbose_name="Subtítulo"
    )
    content = RichTextField(verbose_name="Conteúdo")
    
    # SEO
    meta_title = models.CharField(
        max_length=60, 
        blank=True, 
        verbose_name="Meta Título"
    )
    meta_description = models.CharField(
        max_length=160, 
        blank=True, 
        verbose_name="Meta Descrição"
    )
    
    # Configurações
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    show_in_menu = models.BooleanField(
        default=True, 
        verbose_name="Exibir no Menu"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Página Editável"
        verbose_name_plural = "Páginas Editáveis"
        ordering = ['page_type']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description and self.subtitle:
            self.meta_description = self.subtitle
        super().save(*args, **kwargs)


class SiteConfiguration(models.Model):
    """
    Configurações gerais do site
    """
    site_name = models.CharField(
        max_length=100, 
        default="Conexão Adventure",
        verbose_name="Nome do Site"
    )
    site_description = models.TextField(
        blank=True,
        verbose_name="Descrição do Site"
    )
    
    # Contatos
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    address = models.TextField(blank=True, verbose_name="Endereço")
    
    # Redes sociais
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube")
    
    # Configurações de e-mail
    contact_email = models.EmailField(
        blank=True,
        verbose_name="E-mail de Contato",
        help_text="E-mail que recebe mensagens do formulário de contato"
    )
    notification_email = models.EmailField(
        blank=True,
        verbose_name="E-mail de Notificação",
        help_text="E-mail que recebe notificações de novas inscrições"
    )
    
    # Logos e imagens
    logo = models.ImageField(
        upload_to='site/', 
        blank=True, 
        null=True,
        verbose_name="Logo"
    )
    favicon = models.ImageField(
        upload_to='site/', 
        blank=True, 
        null=True,
        verbose_name="Favicon"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configurações do Site"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Garantir que só existe uma instância
        if not self.pk and SiteConfiguration.objects.exists():
            raise ValidationError('Só pode existir uma configuração do site.')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        """Método para obter a configuração atual"""
        config, created = cls.objects.get_or_create(pk=1)
        return config
