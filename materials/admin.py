from django.contrib import admin
from .models import MaterialCategory, Material, MaterialDownload, MaterialAccess


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'color', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'file_type', 'access_level', 'is_active', 'is_featured', 'order', 'download_count']
    list_filter = ['category', 'file_type', 'access_level', 'is_active', 'is_featured']
    search_fields = ['title', 'description', 'tags']
    list_editable = ['is_active', 'is_featured', 'order']
    readonly_fields = ['download_count', 'file_size', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'description', 'category', 'file_type')
        }),
        ('Arquivo/URL', {
            'fields': ('file', 'external_url', 'thumbnail')
        }),
        ('Configurações de Acesso', {
            'fields': ('access_level', 'requires_registration')
        }),
        ('Configurações de Exibição', {
            'fields': ('is_active', 'is_featured', 'order', 'tags')
        }),
        ('Metadados (Somente Leitura)', {
            'fields': ('file_size', 'download_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MaterialDownload)
class MaterialDownloadAdmin(admin.ModelAdmin):
    list_display = ['material', 'user', 'guest_name', 'guest_email', 'downloaded_at']
    list_filter = ['downloaded_at', 'material__category']
    search_fields = ['material__title', 'user__username', 'guest_name', 'guest_email']
    readonly_fields = ['downloaded_at']
    date_hierarchy = 'downloaded_at'


@admin.register(MaterialAccess)
class MaterialAccessAdmin(admin.ModelAdmin):
    list_display = ['material', 'user', 'granted_at', 'expires_at', 'is_active', 'is_valid']
    list_filter = ['is_active', 'granted_at', 'expires_at']
    search_fields = ['material__title', 'user__username']
    readonly_fields = ['granted_at', 'is_expired', 'is_valid']
