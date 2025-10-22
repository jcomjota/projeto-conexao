from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from django.http import HttpResponseRedirect
from .models import (
    Category, Subcategory, Adventure, AdventureImage, PricingTier
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Administração para categorias de aventuras
    """
    list_display = ['name', 'slug', 'color_display', 'icon_display', 'is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Visual', {
            'fields': ('icon', 'color')
        }),
        ('Configurações', {
            'fields': ('is_active', 'order')
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def color_display(self, obj):
        if obj.color:
            return format_html(
                '<div style="width: 30px; height: 20px; background-color: {}; border: 1px solid #ccc; display: inline-block;"></div> {}',
                obj.color, obj.color
            )
        return '-'
    color_display.short_description = 'Cor'
    
    def icon_display(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 18px;"></i> {}', obj.icon, obj.icon)
        return '-'
    icon_display.short_description = 'Ícone'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """
    Administração para subcategorias
    """
    list_display = ['name', 'category', 'slug', 'is_active', 'order']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Configurações', {
            'fields': ('is_active', 'order')
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class AdventureImageInline(admin.TabularInline):
    """
    Inline para imagens da aventura
    """
    model = AdventureImage
    extra = 0
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview', 'title', 'description', 'order', 'is_cover']
    classes = ['adventure-images-inline']
    template = 'admin/adventures/adventure/tabular_images.html'
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "Sem imagem"
    image_preview.short_description = "Prévia"
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.template = 'admin/adventures/adventure/tabular_images.html'
        return formset


class PricingTierInline(admin.TabularInline):
    """
    Inline para faixas de preço
    """
    model = PricingTier
    extra = 1
    fields = ['name', 'price', 'start_date', 'end_date', 'discount_percentage', 'is_active']


@admin.register(Adventure)
class AdventureAdmin(SummernoteModelAdmin):
    """
    Administração completa para aventuras
    """
    list_display = [
        'title', 'category', 'difficulty', 'duration_hours', 
        'current_price_display', 'is_featured', 'is_active', 'created_at',
        'delete_button'
    ]
    list_filter = [
        'category', 'subcategory', 'difficulty', 'is_featured', 
        'is_active', 'show_in_listing', 'created_at'
    ]
    search_fields = ['title', 'short_description', 'location']
    readonly_fields = ['created_at', 'updated_at', 'current_price_display']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AdventureImageInline, PricingTierInline]
    
    def delete_button(self, obj):
        """Adiciona botão para apagar a aventura diretamente da lista"""
        url = reverse('admin:adventures_adventure_delete', args=[obj.id])
        return format_html('<a class="button" href="{}">Apagar</a>', url)
    delete_button.short_description = 'Ações'
    
    class Media:
        css = {
            'all': ('admin/css/adventure_images.css',)
        }
    
    # Campos que usam Summernote
    summernote_fields = (
        'description', 'what_includes', 'what_to_bring', 
        'safety_requirements', 'additional_info'
    )
    
    class Media:
        css = {
            'all': ('admin/css/adventure_images.css',)
        }
        js = ('admin/js/sortable.min.js',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'title', 'slug', 'category', 'subcategory',
                'short_description', 'description'
            )
        }),
        ('Configurações da Aventura', {
            'fields': (
                'difficulty', 'duration_hours', 
                'min_participants', 'max_participants'
            )
        }),
        ('Localização', {
            'fields': (
                'location', 'meeting_point', 
                'coordinates_lat', 'coordinates_lng'
            )
        }),
        ('Preços', {
            'fields': ('base_price', 'current_price_display')
        }),
        ('Conteúdo Detalhado', {
            'fields': (
                'what_includes', 'what_to_bring', 
                'safety_requirements', 'additional_info'
            )
        }),
        ('Imagem Principal', {
            'fields': ('main_image',)
        }),
        ('Configurações de Exibição', {
            'fields': ('is_featured', 'is_active', 'show_in_listing')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def current_price_display(self, obj):
        price = obj.current_price
        if price != obj.base_price:
            return format_html(
                '<span style="color: red; text-decoration: line-through;">R$ {}</span><br>'
                '<span style="color: green; font-weight: bold;">R$ {}</span>',
                obj.base_price, price
            )
        return f"R$ {price}"
    current_price_display.short_description = "Preço Atual"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'subcategory')
    
    def has_add_permission(self, request):
        return True
    
    def save_model(self, request, obj, form, change):
        """Salva o modelo e processa as imagens da galeria"""
        super().save_model(request, obj, form, change)
        
        # Processa as imagens da galeria após salvar o objeto principal
        if request.FILES.getlist('images'):
            self.process_uploaded_images(request, obj.id)
    
    def process_uploaded_images(self, request, adventure_id):
        """Processa imagens enviadas sem salvar a aventura"""
        if 'images' in request.FILES:
            for image_file in request.FILES.getlist('images'):
                AdventureImage.objects.create(
                    adventure_id=adventure_id,
                    image=image_file
                )
            return True
        return False
        
    def save_model(self, request, obj, form, change):
        """Sobrescreve o método save_model para garantir que as imagens sejam salvas"""
        super().save_model(request, obj, form, change)
        # Processa as imagens após salvar o modelo
        if 'images' in request.FILES:
            self.process_uploaded_images(request, obj.id)
    
    # Removendo os métodos add_view e change_view personalizados para permitir
    # que o Django processe o formulário normalmente


@admin.register(AdventureImage)
class AdventureImageAdmin(admin.ModelAdmin):
    """
    Administração para imagens das aventuras
    """
    list_display = ['adventure', 'title', 'image_preview', 'order', 'is_cover', 'created_at']
    list_filter = ['adventure', 'is_cover', 'created_at']
    search_fields = ['adventure__title', 'title', 'description']
    readonly_fields = ['image_preview', 'created_at']
    
    fieldsets = (
        ('Aventura', {
            'fields': ('adventure',)
        }),
        ('Imagem', {
            'fields': ('image', 'image_preview')
        }),
        ('Informações', {
            'fields': ('title', 'description', 'order', 'is_cover')
        }),
        ('Metadados', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.image.url
            )
        return "Sem imagem"
    image_preview.short_description = "Preview da Imagem"


@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    """
    Administração para faixas de preço
    """
    list_display = [
        'adventure', 'name', 'price', 'start_date', 'end_date', 
        'is_current_display', 'is_active'
    ]
    list_filter = ['adventure', 'is_active', 'start_date', 'end_date']
    search_fields = ['adventure__title', 'name']
    readonly_fields = ['created_at', 'updated_at', 'is_current_display', 'savings_amount_display']
    
    fieldsets = (
        ('Aventura', {
            'fields': ('adventure',)
        }),
        ('Faixa de Preço', {
            'fields': ('name', 'price', 'discount_percentage')
        }),
        ('Período', {
            'fields': ('start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('is_active', 'is_current_display')
        }),
        ('Economia', {
            'fields': ('savings_amount_display',),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_current_display(self, obj):
        if obj.is_current:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Ativo</span>'
            )
        return format_html(
            '<span style="color: gray;">○ Inativo</span>'
        )
    is_current_display.short_description = "Status Atual"
    
    def savings_amount_display(self, obj):
        savings = obj.savings_amount
        if savings > 0:
            return format_html(
                '<span style="color: green;">R$ {:.2f} de economia</span>',
                savings
            )
        return "Sem desconto"
    savings_amount_display.short_description = "Economia"


# Configurações extras do admin
admin.site.site_header = "Conexão Adventure - Administração"
admin.site.site_title = "Conexão Adventure Admin"
admin.site.index_title = "Painel de Administração"
