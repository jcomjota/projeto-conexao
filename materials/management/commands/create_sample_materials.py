from django.core.management.base import BaseCommand
from materials.models import MaterialCategory, Material


class Command(BaseCommand):
    help = 'Cria materiais de exemplo para testar a página'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Criando categorias de materiais...'))
        
        # Criar categorias
        categories_data = [
            {
                'name': 'Documentos',
                'slug': 'documents',
                'description': 'PDFs e documentos importantes',
                'icon': 'fas fa-file-pdf',
                'color': '#dc3545'
            },
            {
                'name': 'Vídeos',
                'slug': 'videos',
                'description': 'Vídeos educativos e tutoriais',
                'icon': 'fas fa-play-circle',
                'color': '#28a745'
            },
            {
                'name': 'Fotos',
                'slug': 'photos',
                'description': 'Galeria de fotos',
                'icon': 'fas fa-camera',
                'color': '#007bff'
            },
            {
                'name': 'Guias',
                'slug': 'guides',
                'description': 'Guias e manuais',
                'icon': 'fas fa-map',
                'color': '#ffc107'
            },
            {
                'name': 'Formulários',
                'slug': 'forms',
                'description': 'Formulários para download',
                'icon': 'fas fa-clipboard-list',
                'color': '#6f42c1'
            }
        ]
        
        for cat_data in categories_data:
            category, created = MaterialCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✓ Categoria criada: {category.name}')
            else:
                self.stdout.write(f'- Categoria já existe: {category.name}')
        
        self.stdout.write(self.style.SUCCESS('Criando materiais de exemplo...'))
        
        # Criar materiais de exemplo
        materials_data = [
            {
                'title': 'Manual de Segurança',
                'description': 'Guia completo de segurança para aventuras. Contém informações essenciais sobre equipamentos de proteção, procedimentos de emergência e boas práticas.',
                'category_slug': 'documents',
                'file_type': 'pdf',
                'tags': 'segurança, manual, equipamentos, emergência',
                'is_featured': True,
                'file_size': 2621440  # 2.5 MB
            },
            {
                'title': 'Regulamento Geral',
                'description': 'Regras e normas para participação em aventuras. Documento oficial com todas as diretrizes e políticas da empresa.',
                'category_slug': 'documents',
                'file_type': 'pdf',
                'tags': 'regulamento, regras, normas, política',
                'file_size': 1887436  # 1.8 MB
            },
            {
                'title': 'Vídeo: Técnicas de Segurança',
                'description': 'Tutorial completo sobre técnicas de segurança em aventuras. Demonstrações práticas de uso de equipamentos e procedimentos.',
                'category_slug': 'videos',
                'file_type': 'video',
                'tags': 'vídeo, tutorial, segurança, técnicas',
                'external_url': 'https://www.youtube.com/watch?v=exemplo',
                'file_size': 89128960  # 85 MB
            },
            {
                'title': 'Vídeo: Como Usar Equipamentos',
                'description': 'Demonstração prática do uso correto dos equipamentos de aventura. Passo a passo detalhado para iniciantes.',
                'category_slug': 'videos',
                'file_type': 'video',
                'tags': 'vídeo, equipamentos, tutorial, iniciantes',
                'external_url': 'https://www.youtube.com/watch?v=exemplo2',
                'file_size': 125829120  # 120 MB
            },
            {
                'title': 'Pack Fotos: Equipamentos',
                'description': 'Galeria com todos os equipamentos utilizados nas aventuras. Imagens em alta resolução para referência.',
                'category_slug': 'photos',
                'file_type': 'image',
                'tags': 'fotos, equipamentos, galeria, referência',
                'file_size': 26214400  # 25 MB
            },
            {
                'title': 'Pack Fotos: Técnicas',
                'description': 'Imagens demonstrativas de técnicas de aventura. Material visual para apoio ao aprendizado.',
                'category_slug': 'photos',
                'file_type': 'image',
                'tags': 'fotos, técnicas, demonstração, aprendizado',
                'file_size': 18874368  # 18 MB
            },
            {
                'title': 'Guia de Equipamentos',
                'description': 'Lista completa de equipamentos necessários para cada tipo de aventura. Inclui especificações técnicas e recomendações.',
                'category_slug': 'guides',
                'file_type': 'pdf',
                'tags': 'guia, equipamentos, lista, especificações',
                'file_size': 3355443  # 3.2 MB
            },
            {
                'title': 'Guia de Trilhas',
                'description': 'Mapas e descrições detalhadas das trilhas disponíveis. Informações sobre dificuldade, duração e pontos de interesse.',
                'category_slug': 'guides',
                'file_type': 'pdf',
                'tags': 'guia, trilhas, mapas, dificuldade',
                'file_size': 9126805  # 8.7 MB
            },
            {
                'title': 'Ficha de Inscrição',
                'description': 'Formulário padrão para inscrição em aventuras. Documento em PDF editável para preenchimento.',
                'category_slug': 'forms',
                'file_type': 'pdf',
                'tags': 'formulário, inscrição, ficha, cadastro',
                'file_size': 1258291  # 1.2 MB
            },
            {
                'title': 'Termo de Responsabilidade',
                'description': 'Documento obrigatório para participação em aventuras. Termo de responsabilidade e isenção de riscos.',
                'category_slug': 'forms',
                'file_type': 'pdf',
                'tags': 'termo, responsabilidade, obrigatório, risco',
                'file_size': 972800  # 950 KB
            }
        ]
        
        for mat_data in materials_data:
            category = MaterialCategory.objects.get(slug=mat_data['category_slug'])
            
            material_dict = {
                'title': mat_data['title'],
                'description': mat_data['description'],
                'category': category,
                'file_type': mat_data['file_type'],
                'tags': mat_data['tags'],
                'file_size': mat_data['file_size'],
                'is_featured': mat_data.get('is_featured', False),
                'access_level': 'public',
                'requires_registration': False
            }
            
            if 'external_url' in mat_data:
                material_dict['external_url'] = mat_data['external_url']
            
            material, created = Material.objects.get_or_create(
                title=mat_data['title'],
                defaults=material_dict
            )
            
            if created:
                self.stdout.write(f'✓ Material criado: {material.title}')
            else:
                self.stdout.write(f'- Material já existe: {material.title}')
        
        self.stdout.write(self.style.SUCCESS('Dados de exemplo criados com sucesso!'))
        self.stdout.write(self.style.SUCCESS('Acesse /materiais/ para ver os resultados.')) 