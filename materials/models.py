from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
import os


User = get_user_model()


class MaterialCategory(models.Model):
    """
    Categorias para organizar os materiais de apoio
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Descrição")
    icon = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="Ícone",
        help_text="Classe CSS do ícone FontAwesome (ex: fas fa-file-pdf)"
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
        verbose_name = "Categoria de Material"
        verbose_name_plural = "Categorias de Materiais"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Material(models.Model):
    """
    Modelo principal para materiais de apoio (PDFs, vídeos, imagens, etc.)
    """
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('video', 'Vídeo'),
        ('image', 'Imagem'),
        ('document', 'Documento'),
        ('presentation', 'Apresentação'),
        ('link', 'Link Externo'),
    ]
    
    ACCESS_LEVEL_CHOICES = [
        ('public', 'Público'),
        ('registered', 'Usuários Registrados'),
        ('premium', 'Premium'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    category = models.ForeignKey(
        MaterialCategory, 
        on_delete=models.CASCADE, 
        related_name='materials',
        verbose_name="Categoria"
    )
    
    file_type = models.CharField(
        max_length=20, 
        choices=FILE_TYPE_CHOICES,
        verbose_name="Tipo de Arquivo"
    )
    
    # Para arquivos locais
    file = models.FileField(
        upload_to='materials/', 
        blank=True, 
        null=True,
        verbose_name="Arquivo",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
                    'mp4', 'webm', 'avi', 'mov',
                    'jpg', 'jpeg', 'png', 'gif', 'webp',
                    'zip', 'rar', '7z'
                ]
            )
        ]
    )
    
    # Para links externos
    external_url = models.URLField(
        blank=True,
        verbose_name="URL Externa",
        help_text="Para vídeos do YouTube, links externos, etc."
    )
    
    # Thumbnail/Preview
    thumbnail = models.ImageField(
        upload_to='materials/thumbnails/', 
        blank=True, 
        null=True,
        verbose_name="Thumbnail/Preview"
    )
    
    # Configurações de acesso
    access_level = models.CharField(
        max_length=20, 
        choices=ACCESS_LEVEL_CHOICES, 
        default='registered',
        verbose_name="Nível de Acesso"
    )
    requires_registration = models.BooleanField(
        default=True, 
        verbose_name="Requer Cadastro"
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
    
    # Metadados
    file_size = models.BigIntegerField(
        null=True, 
        blank=True,
        verbose_name="Tamanho do Arquivo (bytes)"
    )
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Contagem de Downloads"
    )
    
    # Tags para busca
    tags = models.CharField(
        max_length=500, 
        blank=True,
        verbose_name="Tags",
        help_text="Palavras-chave separadas por vírgula para facilitar a busca"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Material de Apoio"
        verbose_name_plural = "Materiais de Apoio"
        ordering = ['-is_featured', 'order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Calcular tamanho do arquivo se não foi definido
        if self.file and not self.file_size:
            try:
                self.file_size = self.file.size
            except Exception:
                pass
        super().save(*args, **kwargs)
    
    @property
    def file_size_formatted(self):
        """Retorna tamanho do arquivo formatado"""
        if not self.file_size:
            return "N/A"
        
        # Converter bytes para MB
        size_mb = self.file_size / (1024 * 1024)
        if size_mb < 1:
            size_kb = self.file_size / 1024
            return f"{size_kb:.1f} KB"
        else:
            return f"{size_mb:.1f} MB"
    
    @property
    def file_extension(self):
        """Retorna extensão do arquivo"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ""
    
    def can_access(self, user):
        """Verifica se o usuário pode acessar o material"""
        if not self.is_active:
            return False
        
        if self.access_level == 'public':
            return True
        
        if self.access_level == 'registered' and user.is_authenticated:
            return True
        
        if self.access_level == 'premium' and user.is_authenticated:
            # Aqui você pode implementar lógica específica para usuários premium
            return user.is_staff or hasattr(user, 'is_premium')
        
        return False


class MaterialDownload(models.Model):
    """
    Registro de downloads para analytics e controle
    """
    material = models.ForeignKey(
        Material, 
        on_delete=models.CASCADE, 
        related_name='downloads',
        verbose_name="Material"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Usuário"
    )
    
    # Informações do usuário não registrado (se aplicável)
    guest_name = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Nome do Visitante"
    )
    guest_email = models.EmailField(
        blank=True,
        verbose_name="E-mail do Visitante"
    )
    
    # Metadados da sessão
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True,
        verbose_name="Endereço IP"
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name="User Agent"
    )
    
    downloaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Download de Material"
        verbose_name_plural = "Downloads de Materiais"
        ordering = ['-downloaded_at']
    
    def __str__(self):
        user_info = self.user.get_full_name() if self.user else (
            self.guest_name or self.guest_email or "Usuário Anônimo"
        )
        return f"{self.material.title} - {user_info}"


class MaterialAccess(models.Model):
    """
    Controle de acesso específico por usuário/material
    """
    material = models.ForeignKey(
        Material, 
        on_delete=models.CASCADE, 
        related_name='access_controls',
        verbose_name="Material"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Usuário"
    )
    
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Expira em"
    )
    granted_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='granted_accesses',
        verbose_name="Concedido por"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    
    class Meta:
        verbose_name = "Acesso a Material"
        verbose_name_plural = "Acessos a Materiais"
        unique_together = ['material', 'user']
        ordering = ['-granted_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.material.title}"
    
    @property
    def is_expired(self):
        """Verifica se o acesso expirou"""
        if not self.expires_at:
            return False
        
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    @property
    def is_valid(self):
        """Verifica se o acesso está válido"""
        return self.is_active and not self.is_expired
