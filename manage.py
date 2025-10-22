#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Verificar se estamos no ambiente de produção ou desenvolvimento
    if os.path.exists(os.path.join(os.path.dirname(__file__), 'settings_production.py')):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_production')
    else:
        # Tentar usar configurações locais
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def create_sample_data():
    """Criar dados de exemplo"""
    from django.contrib.auth import get_user_model
    from adventures.models import AdventureCategory, Adventure, AdventureImage
    from materials.models import MaterialCategory, Material
    from content.models import SiteConfiguration, Banner, Testimonial
    
    User = get_user_model()
    
    print("🚀 Criando dados de exemplo...")
    
    # 1. Criar categorias de aventuras
    rapel_cat, _ = AdventureCategory.objects.get_or_create(
        name="Rapel",
        defaults={'description': "Aventuras de rapel em cachoeiras e paredões"}
    )
    
    trekking_cat, _ = AdventureCategory.objects.get_or_create(
        name="Trekking",
        defaults={'description': "Caminhadas e trilhas pela natureza"}
    )
    
    # 2. Criar aventuras
    cascata_vinho, _ = Adventure.objects.get_or_create(
        title="Cascata do Vinho",
        defaults={
            'category': rapel_cat,
            'description': "Uma experiência incrível de rapel na famosa Cascata do Vinho.",
            'difficulty_level': 'intermediate',
            'duration_hours': 8,
            'min_participants': 4,
            'max_participants': 12,
            'base_price': 180.00,
            'includes': "Transporte, equipamentos, guia especializado, seguro",
            'not_includes': "Alimentação, bebidas",
            'what_to_bring': "Roupa confortável, tênis, protetor solar, água",
            'meeting_point': "Centro de Bento Gonçalves",
            'is_active': True,
        }
    )
    
    jaboticaba, _ = Adventure.objects.get_or_create(
        title="Rapel Estação Jaboticaba",
        defaults={
            'category': rapel_cat,
            'description': "Rapel emocionante na Estação Jaboticaba.",
            'difficulty_level': 'advanced',
            'duration_hours': 6,
            'min_participants': 2,
            'max_participants': 8,
            'base_price': 220.00,
            'includes': "Transporte, equipamentos, guia especializado, seguro",
            'not_includes': "Alimentação, bebidas",
            'what_to_bring': "Roupa confortável, tênis, protetor solar, água",
            'meeting_point': "Estação Jaboticaba",
            'is_active': True,
        }
    )
    
    pompeia, _ = Adventure.objects.get_or_create(
        title="Cascata Pompeia",
        defaults={
            'category': rapel_cat,
            'description': "Rapel e cachoeirismo na bela Cascata Pompeia.",
            'difficulty_level': 'beginner',
            'duration_hours': 7,
            'min_participants': 3,
            'max_participants': 10,
            'base_price': 160.00,
            'includes': "Transporte, equipamentos, guia especializado, seguro",
            'not_includes': "Alimentação, bebidas",
            'what_to_bring': "Roupa confortável, tênis, protetor solar, água",
            'meeting_point': "Centro de Garibaldi",
            'is_active': True,
        }
    )
    
    # 3. Criar categorias de materiais
    checklist_cat, _ = MaterialCategory.objects.get_or_create(
        name="Checklists",
        defaults={'description': "Listas de verificação para suas aventuras"}
    )
    
    guias_cat, _ = MaterialCategory.objects.get_or_create(
        name="Guias",
        defaults={'description': "Guias e manuais para atividades de aventura"}
    )
    
    # 4. Criar materiais
    Material.objects.get_or_create(
        title="Checklist para Rapel",
        defaults={
            'category': checklist_cat,
            'description': "Lista completa de equipamentos e preparativos para rapel",
            'content': "- Equipamentos de segurança\n- Roupas adequadas\n- Documentos",
            'file_type': 'pdf',
            'is_active': True,
        }
    )
    
    Material.objects.get_or_create(
        title="Guia de Segurança",
        defaults={
            'category': guias_cat,
            'description': "Manual completo de segurança para atividades de aventura",
            'content': "Normas de segurança e procedimentos de emergência",
            'file_type': 'pdf',
            'is_active': True,
        }
    )
    
    # 5. Configuração do site
    config, _ = SiteConfiguration.objects.get_or_create(
        defaults={
            'site_name': "Conexão Adventure",
            'site_description': "Aventuras incríveis, experiências inesquecíveis",
            'contact_email': "contato@conexaoadventure.com.br",
            'contact_phone': "(51) 3333-4444",
            'whatsapp_number': "5551999999999",
            'facebook_url': "https://facebook.com/conexaoadventure",
            'instagram_url': "https://instagram.com/conexaoadventure",
        }
    )
    
    print("✅ Dados de exemplo criados com sucesso!")


if __name__ == '__main__':
    main()
