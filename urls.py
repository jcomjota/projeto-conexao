"""
Configurações de URL para o projeto Conexão Adventure.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aventuras/', include('adventures.urls')),
    path('reservas/', include('bookings.urls')),
    path('', include('content.urls')),
    path('materiais/', include('materials.urls')),
    path('servicos/', include('services.urls')),
    path('usuarios/', include('users.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Servir arquivos estáticos e de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)