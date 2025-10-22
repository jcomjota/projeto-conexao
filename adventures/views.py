from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from .models import Adventure, Category, AdventureImage
import json


class AdventureListView(ListView):
    """
    Lista de todas as aventuras
    """
    model = Adventure
    template_name = 'adventures/list.html'
    context_object_name = 'adventures'
    paginate_by = 12
    
    def get_queryset(self):
        return Adventure.objects.filter(
            is_active=True, 
            show_in_listing=True
        ).select_related('category', 'subcategory').order_by('-is_featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).order_by('order', 'name')
        return context


class AdventureDetailView(DetailView):
    """
    Detalhes de uma aventura específica
    """
    model = Adventure
    template_name = 'adventures/detail.html'
    context_object_name = 'adventure'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Adventure.objects.filter(is_active=True).select_related(
            'category', 'subcategory'
        ).prefetch_related('images', 'pricing_tiers')


class CategoryListView(ListView):
    """
    Lista de aventuras por categoria
    """
    model = Adventure
    template_name = 'adventures/category.html'
    
@staff_member_required
def upload_adventure_image(request, adventure_id=None):
    """
    View para upload de imagens via AJAX no admin
    """
    if request.method != 'POST' or not request.FILES.get('image'):
        return JsonResponse({'success': False, 'error': 'Método inválido ou nenhuma imagem enviada'})
    
    try:
        # Se não tiver adventure_id, estamos criando uma nova aventura
        # Neste caso, criamos uma imagem temporária que será associada depois
        adventure = None
        if adventure_id:
            adventure = Adventure.objects.get(id=adventure_id)
        
        # Cria a imagem
        image = AdventureImage(adventure=adventure)
        image.image = request.FILES['image']
        image.save()
        
        return JsonResponse({
            'success': True,
            'image_id': image.id,
            'image_url': image.image.url
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    context_object_name = 'adventures'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        return Adventure.objects.filter(
            category=self.category,
            is_active=True,
            show_in_listing=True
        ).select_related('category', 'subcategory').order_by('-is_featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.filter(is_active=True).order_by('order', 'name')
        return context
