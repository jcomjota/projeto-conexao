from .models import SiteConfiguration


def site_content(request):
    """
    Context processor para disponibilizar configurações do site
    em todos os templates
    """
    try:
        config = SiteConfiguration.get_config()
        return {
            'site_config': config,
            'site_name': config.site_name,
            'site_description': config.site_description,
            'contact_info': {
                'phone': config.phone,
                'whatsapp': config.whatsapp,
                'email': config.email,
                'address': config.address,
            },
            'social_media': {
                'facebook': config.facebook_url,
                'instagram': config.instagram_url,
                'youtube': config.youtube_url,
            }
        }
    except Exception:
        # Fallback em caso de erro
        return {
            'site_config': None,
            'site_name': 'Conexão Adventure',
            'site_description': 'Aventuras inesquecíveis em meio à natureza',
            'contact_info': {
                'phone': '',
                'whatsapp': '',
                'email': '',
                'address': '',
            },
            'social_media': {
                'facebook': '',
                'instagram': '',
                'youtube': '',
            }
        } 