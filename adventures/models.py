from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta
from ckeditor.fields import RichTextField


class Category(models.Model):
    """
    Categorias de aventuras (ex: Rapel, Trekking, Cachoeirismo)
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Descrição")
    icon = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="Ícone",
        help_text="Classe CSS do ícone FontAwesome (ex: fas fa-mountain)"
    )
    color = models.CharField(
        max_length=7, 
        default='#007bff', 
        verbose_name="Cor",
        help_text="Cor hexadecimal para representar a categoria"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Subcategorias de aventuras para organização mais específica
    """
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='subcategories',
        verbose_name="Categoria"
    )
    name = models.CharField(max_length=100, verbose_name="Nome")
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField(blank=True, verbose_name="Descrição")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Subcategoria"
        verbose_name_plural = "Subcategorias"
        ordering = ['order', 'name']
        unique_together = ['category', 'slug']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Adventure(models.Model):
    """
    Modelo principal para as aventuras/programações
    """
    DIFFICULTY_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('moderado', 'Moderado'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
        ('expert', 'Expert'),
    ]
    
    # Informações básicas
    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='adventures',
        verbose_name="Categoria"
    )
    subcategory = models.ForeignKey(
        Subcategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='adventures',
        verbose_name="Subcategoria"
    )
    
    # Descrições
    short_description = models.CharField(
        max_length=300, 
        verbose_name="Descrição Curta",
        help_text="Descrição que aparece na listagem de aventuras"
    )
    description = RichTextField(verbose_name="Descrição Completa")
    
    # Configurações da aventura
    difficulty = models.CharField(
        max_length=20, 
        choices=DIFFICULTY_CHOICES, 
        verbose_name="Nível de Dificuldade"
    )
    duration_hours = models.PositiveIntegerField(
        verbose_name="Duração (horas)",
        validators=[MinValueValidator(1), MaxValueValidator(720)]
    )
    min_participants = models.PositiveIntegerField(
        default=4, 
        verbose_name="Mínimo de Participantes"
    )
    max_participants = models.PositiveIntegerField(
        default=20, 
        verbose_name="Máximo de Participantes"
    )
    
    # Localização
    location = models.CharField(max_length=200, verbose_name="Localização")
    meeting_point = models.TextField(verbose_name="Ponto de Encontro")
    coordinates_lat = models.DecimalField(
        max_digits=10, 
        decimal_places=8, 
        null=True, 
        blank=True,
        verbose_name="Latitude"
    )
    coordinates_lng = models.DecimalField(
        max_digits=11, 
        decimal_places=8, 
        null=True, 
        blank=True,
        verbose_name="Longitude"
    )
    
    # Preços (sistema dinâmico)
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço Base"
    )
    
    # Conteúdo detalhado
    what_includes = RichTextField(
        verbose_name="O que está incluído",
        help_text="Liste tudo que está incluído na aventura"
    )
    what_to_bring = RichTextField(
        verbose_name="O que levar",
        help_text="Lista do que o participante deve levar"
    )
    safety_requirements = RichTextField(
        verbose_name="Requisitos de Segurança",
        help_text="Informações importantes sobre segurança"
    )
    additional_info = RichTextField(
        blank=True,
        verbose_name="Informações Adicionais"
    )
    
    # Configurações de exibição
    is_featured = models.BooleanField(
        default=False, 
        verbose_name="Destacar na Home Page"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    show_in_listing = models.BooleanField(
        default=True, 
        verbose_name="Exibir na Listagem"
    )
    
    # Imagem principal
    main_image = models.ImageField(
        upload_to='adventures/main/', 
        verbose_name="Imagem Principal"
    )
    
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
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Aventura"
        verbose_name_plural = "Aventuras"
        ordering = ['-is_featured', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = self.short_description
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('adventure_detail', kwargs={'slug': self.slug})
    
    @property
    def current_price(self):
        """Retorna o preço atual considerando os descontos dinâmicos"""
        try:
            current_pricing = self.pricing_tiers.filter(
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now(),
                is_active=True
            ).first()
            
            if current_pricing:
                return current_pricing.price
            return self.base_price
        except Exception:
            return self.base_price
    
    @property
    def next_price_change(self):
        """Retorna a próxima mudança de preço"""
        try:
            next_tier = self.pricing_tiers.filter(
                start_date__gt=timezone.now(),
                is_active=True
            ).order_by('start_date').first()
            return next_tier
        except Exception:
            return None
    
    @property
    def next_event(self):
        """Retorna o próximo evento disponível para esta aventura"""
        try:
            from django.utils import timezone
            return self.events.filter(
                date__gte=timezone.now().date(),
                is_active=True,
                status='scheduled'
            ).order_by('date', 'start_time').first()
        except Exception:
            return None


class AdventureImage(models.Model):
    """
    Galeria de imagens para cada aventura
    """
    adventure = models.ForeignKey(
        Adventure, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Aventura"
    )
    image = models.ImageField(
        upload_to='adventures/gallery/', 
        verbose_name="Imagem"
    )
    title = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Título"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Descrição"
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Ordem de Exibição"
    )
    is_cover = models.BooleanField(
        default=False, 
        verbose_name="Imagem de Capa"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Imagem da Aventura"
        verbose_name_plural = "Imagens da Aventura"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.adventure.title} - Imagem {self.order}"


class PricingTier(models.Model):
    """
    Sistema de preços dinâmicos por período
    """
    adventure = models.ForeignKey(
        Adventure, 
        on_delete=models.CASCADE, 
        related_name='pricing_tiers',
        verbose_name="Aventura"
    )
    name = models.CharField(
        max_length=100, 
        verbose_name="Nome do Período",
        help_text="Ex: Promoção Antecipada, Preço Normal, Última Hora"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço"
    )
    start_date = models.DateTimeField(verbose_name="Data de Início")
    end_date = models.DateTimeField(verbose_name="Data de Fim")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    
    # Informações de desconto
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Percentual de Desconto",
        help_text="Percentual em relação ao preço base"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Faixa de Preço"
        verbose_name_plural = "Faixas de Preço"
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.adventure.title} - {self.name} (R$ {self.price})"
    
    @property
    def is_current(self):
        """Verifica se esta faixa de preço está ativa no momento"""
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active
    
    @property
    def savings_amount(self):
        """Calcula o valor economizado em relação ao preço base"""
        if self.discount_percentage:
            return self.adventure.base_price - self.price
        return 0
