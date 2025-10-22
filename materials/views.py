from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, FileResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Material, MaterialCategory, MaterialDownload


def MaterialListView(request):
    """Lista de materiais de apoio"""
    # Buscar todas as categorias ativas
    categories = MaterialCategory.objects.filter(is_active=True)
    
    # Buscar todos os materiais ativos
    materials = Material.objects.filter(is_active=True).select_related('category')
    
    # Filtros de pesquisa se houver
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    if search_query:
        materials = materials.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    if category_filter and category_filter != 'all':
        materials = materials.filter(category__slug=category_filter)
    
    # Contar estatísticas
    total_materials = materials.count()
    videos_count = materials.filter(file_type='video').count()
    documents_count = materials.filter(file_type__in=['pdf', 'document']).count()
    
    context = {
        'materials': materials,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'total_materials': total_materials,
        'videos_count': videos_count,
        'documents_count': documents_count,
    }
    
    return render(request, 'materials/list.html', context)


def MaterialCategoryView(request, slug):
    """Lista de materiais por categoria"""
    category = get_object_or_404(MaterialCategory, slug=slug, is_active=True)
    materials = Material.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'materials': materials,
    }
    
    return render(request, 'materials/category.html', context)


def MaterialDownloadView(request, pk):
    """Download de material"""
    material = get_object_or_404(Material, pk=pk, is_active=True)
    
    # Verificar se o usuário pode acessar o material
    if not material.can_access(request.user):
        raise Http404("Material não encontrado ou acesso negado")
    
    # Registrar o download
    download_record = MaterialDownload.objects.create(
        material=material,
        user=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Incrementar contador de downloads
    material.download_count += 1
    material.save(update_fields=['download_count'])
    
    # Se for arquivo local, servir o arquivo
    if material.file:
        return FileResponse(
            material.file.open(),
            as_attachment=True,
            filename=material.file.name.split('/')[-1]
        )
    # Se for link externo, redirecionar
    elif material.external_url:
        from django.shortcuts import redirect
        return redirect(material.external_url)
    
    raise Http404("Arquivo não encontrado")
