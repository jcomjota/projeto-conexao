from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponseRedirect
from .models import CustomUser, UserProfile, Badge, Reward, UserBadge, UserReward


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'requirement_type', 'created_at')
    list_filter = ('requirement_type',)
    search_fields = ('name', 'description')


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_cost', 'reward_type', 'is_active', 'created_at')
    list_filter = ('reward_type', 'is_active')
    search_fields = ('name', 'description')


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'earned_at')
    list_filter = ('badge', 'earned_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'badge__name')
    raw_id_fields = ('user', 'badge')


@admin.register(UserReward)
class UserRewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'reward', 'status', 'redeemed_at', 'used_at')
    list_filter = ('status', 'redeemed_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'reward__name')
    raw_id_fields = ('user', 'reward')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Administração personalizada para usuários
    """
    list_display = [
        'email', 'get_full_name', 'phone', 'experience_level', 
        'total_adventures', 'is_active', 'date_joined', 'change_password_link'
    ]
    list_filter = [
        'is_active', 'is_staff', 'experience_level', 
        'receive_notifications', 'newsletter_subscription', 'date_joined'
    ]
    search_fields = ['email', 'first_name', 'last_name', 'phone', 'cpf']
    readonly_fields = ['date_joined', 'last_login', 'total_adventures']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('username', 'email', 'password')
        }),
        ('Dados Pessoais', {
            'fields': (
                'first_name', 'last_name', 'birth_date', 'cpf',
                'phone', 'address', 'city', 'state', 'zip_code'
            )
        }),
        ('Contato de Emergência', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone'),
            'classes': ('collapse',)
        }),
        ('Aventuras', {
            'fields': ('experience_level', 'total_adventures'),
        }),
        ('Configurações', {
            'fields': (
                'receive_notifications', 'newsletter_subscription',
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
        ('Metadados', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Informações Obrigatórias', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
        ('Informações Adicionais', {
            'classes': ('wide', 'collapse'),
            'fields': ('phone', 'experience_level'),
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.email
    get_full_name.short_description = "Nome Completo"
    
    def total_adventures(self, obj):
        count = obj.total_adventures
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{}</span>',
                count
            )
        return count
    total_adventures.short_description = "Total de Aventuras"
    
    def change_password_link(self, obj):
        """Links para editar e excluir o usuário"""
        if obj.pk:
            edit_url = reverse('admin:users_customuser_change', args=[obj.pk])
            delete_url = reverse('admin:users_customuser_delete', args=[obj.pk])
            return format_html(
                '<a href="{}" class="button editar-btn">Editar</a> '
                '<a href="{}" class="button excluir-btn" style="background-color: #ba2121; color: white;">Excluir</a>', 
                edit_url, delete_url
            )
        return "-"
    change_password_link.short_description = "Ações"
    change_password_link.allow_tags = True
    
    def get_urls(self):
        """Adiciona URLs customizadas para o admin"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/change-password/',
                self.admin_site.admin_view(self.change_user_password_view),
                name='change_user_password',
            ),
        ]
        return custom_urls + urls
    
    def change_user_password_view(self, request, user_id):
        """View para alterar senha do usuário"""
        user = get_object_or_404(CustomUser, pk=user_id)
        
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 
                    f'Senha alterada com sucesso para {user.get_full_name()} ({user.email})'
                )
                return HttpResponseRedirect(reverse('admin:users_customuser_changelist'))
        else:
            form = SetPasswordForm(user)
        
        context = {
            'title': f'Alterar senha para {user.get_full_name()}',
            'form': form,
            'user_obj': user,
            'opts': self.model._meta,
            'has_change_permission': True,
        }
        
        return render(request, 'admin/users/change_password.html', context)


class UserProfileInline(admin.StackedInline):
    """
    Inline para perfil do usuário
    """
    model = UserProfile
    can_delete = False
    verbose_name = "Perfil Adicional"
    verbose_name_plural = "Perfil Adicional"
    
    fieldsets = (
        ('Informações do Perfil', {
            'fields': ('bio', 'avatar')
        }),
        ('Informações Médicas', {
            'fields': ('medical_conditions', 'medications', 'allergies'),
            'classes': ('collapse',)
        }),
        ('Preferências', {
            'fields': ('preferred_activities',),
            'classes': ('collapse',)
        }),
    )


# Adicionar o inline ao admin do usuário  
# CustomUserAdmin.inlines = (UserProfileInline,)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Administração para perfis de usuário
    """
    list_display = ['user', 'get_user_email', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações do Perfil', {
            'fields': ('bio', 'avatar')
        }),
        ('Informações Médicas', {
            'fields': ('medical_conditions', 'medications', 'allergies'),
        }),
        ('Preferências', {
            'fields': ('preferred_activities',),
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = "E-mail"
    get_user_email.admin_order_field = 'user__email'
