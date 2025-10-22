from django.core.management.base import BaseCommand
from adventures.models import Adventure, Category
from decimal import Decimal
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Cria aventuras de teste baseadas nas páginas HTML existentes'

    def handle(self, *args, **options):
        print('Criando aventuras de teste...')
        
        # Criar categorias se não existirem
        category_cachoeira, created = Category.objects.get_or_create(
            name='Cachoeirismo',
            defaults={
                'description': 'Aventuras em cachoeiras com rappel e exploração aquática',
                'is_active': True
            }
        )
        
        category_trilha, created = Category.objects.get_or_create(
            name='Trilhas',
            defaults={
                'description': 'Caminhadas e trilhas em meio à natureza',
                'is_active': True
            }
        )
        
        category_escalada, created = Category.objects.get_or_create(
            name='Escalada',
            defaults={
                'description': 'Escalada em rocha e montanhismo',
                'is_active': True
            }
        )
        
        # Definir aventuras baseadas nas páginas HTML
        adventures_data = [
            {
                'title': 'Cascata do Vinho',
                'short_description': 'Uma das cachoeiras mais espetaculares do Rio Grande do Sul. Mergulhe nesta experiência única de cachoeirismo e contemple a natureza em seu estado mais puro.',
                'description': '''
                <h3>Sobre a Aventura</h3>
                <p>A Cascata do Vinho é uma das mais belas cachoeiras da região da Serra Gaúcha. Com aproximadamente 25 metros de altura, oferece uma experiência única de cachoeirismo em meio à natureza exuberante.</p>
                
                <h3>Observações importantes:</h3>
                <ul>
                    <li>Idade mínima: 14 anos</li>
                    <li>Peso máximo: 120kg</li>
                    <li>Não recomendado para pessoas com medo de altura</li>
                    <li>Atividade sujeita às condições climáticas</li>
                </ul>
                ''',
                'what_includes': '''
                <ul>
                    <li>Equipamentos de segurança (capacete, cadeirinha, freio)</li>
                    <li>Cordas e equipamentos técnicos</li>
                    <li>Instrutor qualificado</li>
                    <li>Seguro de aventura</li>
                    <li>Lanche energético</li>
                </ul>
                ''',
                'what_to_bring': '''
                <ul>
                    <li>Roupa que pode molhar</li>
                    <li>Tênis de trilha ou que pode molhar</li>
                    <li>Roupa de banho</li>
                    <li>Toalha</li>
                    <li>Protetor solar</li>
                    <li>Repelente</li>
                </ul>
                ''',
                'safety_requirements': '''
                <ul>
                    <li>Idade mínima: 14 anos</li>
                    <li>Peso máximo: 120kg</li>
                    <li>Não recomendado para pessoas com medo de altura</li>
                    <li>Atividade sujeita às condições climáticas</li>
                </ul>
                ''',
                'location': 'Bento Gonçalves, RS',
                'meeting_point': 'Estacionamento da Cascata do Vinho - Bento Gonçalves/RS',
                'difficulty': 'intermediario',
                'duration_hours': 4,
                'min_participants': 4,
                'max_participants': 15,
                'base_price': Decimal('180.00'),
                'category': category_cachoeira,
                'is_active': True,
                'is_featured': True,
                'image_file': 'cascata-do-vinho.jpg',
            },
            {
                'title': 'Cascata Pompeia',
                'short_description': 'Uma das cachoeiras mais históricas e imponentes da região. Viva uma experiência única com rappel em meio à natureza exuberante e águas cristalinas.',
                'description': '''
                <h3>Sobre a Aventura</h3>
                <p>A Cascata Pompeia é uma formação rochosa histórica com aproximadamente 35 metros de altura. Localizada em São Francisco de Paula, oferece uma das experiências mais emocionantes de rappel da região.</p>
                
                <h3>Observações importantes:</h3>
                <ul>
                    <li>Idade mínima: 16 anos</li>
                    <li>Experiência prévia recomendada</li>
                    <li>Peso máximo: 110kg</li>
                    <li>Atividade de nível intermediário</li>
                    <li>Sujeita às condições climáticas</li>
                </ul>
                ''',
                'what_includes': '''
                <ul>
                    <li>Equipamentos de segurança completos</li>
                    <li>Cordas estáticas de alta qualidade</li>
                    <li>Instrutor certificado</li>
                    <li>Seguro de aventura</li>
                    <li>Lanche e hidratação</li>
                    <li>Transporte do estacionamento até a cachoeira</li>
                </ul>
                ''',
                'what_to_bring': '''
                <ul>
                    <li>Roupa confortável para atividade física</li>
                    <li>Tênis de trilha</li>
                    <li>Roupa de banho (opcional)</li>
                    <li>Mochila pequena</li>
                    <li>Câmera (à prova d'água)</li>
                    <li>Protetor solar e repelente</li>
                </ul>
                ''',
                'safety_requirements': '''
                <ul>
                    <li>Idade mínima: 16 anos</li>
                    <li>Experiência prévia recomendada</li>
                    <li>Peso máximo: 110kg</li>
                    <li>Atividade de nível intermediário</li>
                    <li>Sujeita às condições climáticas</li>
                </ul>
                ''',
                'location': 'São Francisco de Paula, RS',
                'meeting_point': 'Centro de Visitantes Cascata Pompeia - São Francisco de Paula/RS',
                'difficulty': 'intermediario',
                'duration_hours': 5,
                'min_participants': 6,
                'max_participants': 20,
                'base_price': Decimal('220.00'),
                'category': category_cachoeira,
                'is_active': True,
                'is_featured': True,
                'image_file': 'pompeia.jpg',
            },
            {
                'title': 'Trilha da Jaboticaba',
                'short_description': 'Uma trilha fascinante através da mata nativa, descobrindo nascentes cristalinas e a famosa árvore centenária de jaboticaba.',
                'description': '''
                <h3>Sobre a Aventura</h3>
                <p>A Trilha da Jaboticaba é um percurso de dificuldade moderada que leva os aventureiros através de mata nativa preservada, culminando na descoberta de uma jaboticabeira centenária e nascentes de água cristalina.</p>
                
                <h3>Observações importantes:</h3>
                <ul>
                    <li>Idade mínima: 12 anos</li>
                    <li>Trilha de 8km (ida e volta)</li>
                    <li>Nível de dificuldade: moderado</li>
                    <li>Calçado adequado obrigatório</li>
                    <li>Atividade educativa sobre fauna e flora</li>
                </ul>
                ''',
                'what_includes': '''
                <ul>
                    <li>Guia especializado em fauna e flora</li>
                    <li>Kit de primeiros socorros</li>
                    <li>Lanche de trilha</li>
                    <li>Água e isotônico</li>
                    <li>Seguro de aventura</li>
                </ul>
                ''',
                'what_to_bring': '''
                <ul>
                    <li>Roupa confortável para caminhada</li>
                    <li>Tênis de trilha</li>
                    <li>Mochila</li>
                    <li>Boné ou chapéu</li>
                    <li>Protetor solar</li>
                    <li>Repelente</li>
                    <li>Câmera fotográfica</li>
                </ul>
                ''',
                'safety_requirements': '''
                <ul>
                    <li>Idade mínima: 12 anos</li>
                    <li>Calçado adequado obrigatório</li>
                    <li>Condição física básica necessária</li>
                    <li>Respeitar a fauna e flora local</li>
                </ul>
                ''',
                'location': 'Gramado, RS',
                'meeting_point': 'Portal de Entrada Trilha da Jaboticaba - Gramado/RS',
                'difficulty': 'moderado',
                'duration_hours': 6,
                'min_participants': 5,
                'max_participants': 25,
                'base_price': Decimal('120.00'),
                'category': category_trilha,
                'is_active': True,
                'is_featured': False,
                'image_file': 'jaboticaba.jpg',
            },
            {
                'title': 'Escalada Morro dos Ventos',
                'short_description': 'Desafie seus limites na escalada do Morro dos Ventos, com vista panorâmica de 360° da região serrana do Rio Grande do Sul.',
                'description': '''
                <h3>Sobre a Aventura</h3>
                <p>O Morro dos Ventos oferece uma das melhores vistas panorâmicas da região. Com vias de escalada de diferentes níveis, é ideal tanto para iniciantes quanto para escaladores experientes.</p>
                
                <h3>Observações importantes:</h3>
                <ul>
                    <li>Idade mínima: 14 anos</li>
                    <li>Peso máximo: 100kg</li>
                    <li>Vias para diferentes níveis</li>
                    <li>Instrução técnica incluída</li>
                    <li>Atividade sujeita ao tempo</li>
                </ul>
                ''',
                'what_includes': '''
                <ul>
                    <li>Equipamentos de escalada completos</li>
                    <li>Capacete e cadeirinha de segurança</li>
                    <li>Cordas dinâmicas</li>
                    <li>Instrutor ABETA certificado</li>
                    <li>Seguro de aventura</li>
                    <li>Lanche energético</li>
                </ul>
                ''',
                'what_to_bring': '''
                <ul>
                    <li>Roupa esportiva confortável</li>
                    <li>Tênis de escalada ou esportivo</li>
                    <li>Luvas (opcional)</li>
                    <li>Mochila pequena</li>
                    <li>Protetor solar</li>
                    <li>Água extra</li>
                </ul>
                ''',
                'safety_requirements': '''
                <ul>
                    <li>Idade mínima: 14 anos</li>
                    <li>Peso máximo: 100kg</li>
                    <li>Condição física adequada</li>
                    <li>Não ter medo de altura</li>
                    <li>Seguir instruções do guia</li>
                </ul>
                ''',
                'location': 'Canela, RS',
                'meeting_point': 'Base da Escalada Morro dos Ventos - Canela/RS',
                'difficulty': 'intermediario',
                'duration_hours': 8,
                'min_participants': 3,
                'max_participants': 12,
                'base_price': Decimal('280.00'),
                'category': category_escalada,
                'is_active': True,
                'is_featured': False,
                'image_file': 'escalada.jpg',
            },
            {
                'title': 'Cânion do Itaimbezinho',
                'short_description': 'Explore um dos cânions mais impressionantes do Brasil, com trilhas que revelam paisagens de tirar o fôlego e cachoeiras espetaculares.',
                'description': '''
                <h3>Sobre a Aventura</h3>
                <p>O Cânion do Itaimbezinho é uma das formações geológicas mais impressionantes do sul do Brasil. Com paredes de até 720 metros de altura, oferece trilhas espetaculares e vistas inesquecíveis.</p>
                
                <h3>Observações importantes:</h3>
                <ul>
                    <li>Idade mínima: 10 anos</li>
                    <li>Trilha de 12km total</li>
                    <li>Nível: iniciante a moderado</li>
                    <li>Sujeito às condições do parque</li>
                    <li>Saída bem cedo (6h30)</li>
                </ul>
                ''',
                'what_includes': '''
                <ul>
                    <li>Transporte até o Parque Nacional</li>
                    <li>Guia credenciado do parque</li>
                    <li>Taxa de entrada no parque</li>
                    <li>Lanche de trilha</li>
                    <li>Kit de hidratação</li>
                    <li>Seguro de aventura</li>
                </ul>
                ''',
                'what_to_bring': '''
                <ul>
                    <li>Roupa confortável para caminhada</li>
                    <li>Tênis de trilha obrigatório</li>
                    <li>Agasalho (pode fazer frio)</li>
                    <li>Capa de chuva</li>
                    <li>Protetor solar</li>
                    <li>Câmera fotográfica</li>
                </ul>
                ''',
                'safety_requirements': '''
                <ul>
                    <li>Idade mínima: 10 anos</li>
                    <li>Condição física básica</li>
                    <li>Calçado de trilha obrigatório</li>
                    <li>Respeitar regras do parque</li>
                    <li>Pontualidade no horário de saída</li>
                </ul>
                ''',
                'location': 'Cambará do Sul, RS',
                'meeting_point': 'Centro de Visitantes Parque Nacional Aparados da Serra - Cambará do Sul/RS',
                'difficulty': 'moderado',
                'duration_hours': 10,
                'min_participants': 8,
                'max_participants': 30,
                'base_price': Decimal('160.00'),
                'category': category_trilha,
                'is_active': True,
                'is_featured': True,
                'image_file': 'canion.jpg',
            }
        ]
        
        # Criar aventuras
        created_count = 0
        updated_count = 0
        
        for adventure_data in adventures_data:
            # Extrair o nome do arquivo de imagem
            image_file = adventure_data.pop('image_file', None)
            
            # Verificar se a aventura já existe
            adventure, created = Adventure.objects.get_or_create(
                title=adventure_data['title'],
                defaults=adventure_data
            )
            
            if created:
                created_count += 1
                print(f'✓ Aventura criada: {adventure.title}')
            else:
                # Atualizar dados se já existe
                for key, value in adventure_data.items():
                    if key != 'title':  # Não atualizar o título
                        setattr(adventure, key, value)
                adventure.save()
                updated_count += 1
                print(f'↻ Aventura atualizada: {adventure.title}')
            
            # Adicionar imagem se especificada e ainda não tem
            if image_file and (not adventure.main_image or created):
                image_path = os.path.join('media', 'adventures', 'main', image_file)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        adventure.main_image.save(
                            image_file,
                            File(img_file),
                            save=True
                        )
                    print(f'  📷 Imagem adicionada: {image_file}')
        
        print(f'\n✅ Processo concluído!')
        print(f'• {created_count} aventuras criadas')
        print(f'• {updated_count} aventuras atualizadas') 