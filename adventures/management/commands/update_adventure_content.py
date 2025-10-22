from django.core.management.base import BaseCommand
from adventures.models import Adventure


class Command(BaseCommand):
    help = 'Atualiza o conteúdo das aventuras para o novo layout'

    def handle(self, *args, **options):
        adventures_data = {
            'cascata-do-vinho': {
                'what_includes': '''
                <div class="included-grid">
                    <div class="included-item">
                        <i class="fas fa-user-tie"></i>
                        <div>
                            <h4>Guias Especializados</h4>
                            <p>Profissionais certificados e experientes</p>
                        </div>
                    </div>
                    <div class="included-item">
                        <i class="fas fa-hard-hat"></i>
                        <div>
                            <h4>Equipamentos de Segurança</h4>
                            <p>Capacetes, cordas e equipamentos certificados</p>
                        </div>
                    </div>
                    <div class="included-item">
                        <i class="fas fa-shield-alt"></i>
                        <div>
                            <h4>Seguro contra Acidentes</h4>
                            <p>Cobertura completa durante a atividade</p>
                        </div>
                    </div>
                    <div class="included-item">
                        <i class="fas fa-camera"></i>
                        <div>
                            <h4>Fotos da Aventura</h4>
                            <p>Registro profissional dos melhores momentos</p>
                        </div>
                    </div>
                    <div class="included-item">
                        <i class="fas fa-certificate"></i>
                        <div>
                            <h4>Certificado de Participação</h4>
                            <p>Comprovante da sua conquista</p>
                        </div>
                    </div>
                    <div class="included-item">
                        <i class="fas fa-first-aid"></i>
                        <div>
                            <h4>Kit Primeiros Socorros</h4>
                            <p>Atendimento médico básico disponível</p>
                        </div>
                    </div>
                </div>
                ''',
                'what_to_bring': '''
                <div class="bring-categories">
                    <div class="bring-category">
                        <h4><i class="fas fa-swimming-pool"></i> Para a Água</h4>
                        <ul>
                            <li>Roupa de banho</li>
                            <li>Toalha</li>
                            <li>Chinelo antiderrapante</li>
                        </ul>
                    </div>
                    <div class="bring-category">
                        <h4><i class="fas fa-tshirt"></i> Vestuário</h4>
                        <ul>
                            <li>Roupa confortável</li>
                            <li>Roupa extra (seca)</li>
                            <li>Calçado apropriado para trilha</li>
                        </ul>
                    </div>
                    <div class="bring-category">
                        <h4><i class="fas fa-sun"></i> Proteção</h4>
                        <ul>
                            <li>Protetor solar FPS 30+</li>
                            <li>Repelente</li>
                            <li>Óculos de sol</li>
                            <li>Boné ou chapéu</li>
                        </ul>
                    </div>
                    <div class="bring-category">
                        <h4><i class="fas fa-utensils"></i> Alimentação</h4>
                        <ul>
                            <li>Água (mínimo 1L)</li>
                            <li>Lanche energético</li>
                            <li>Frutas</li>
                        </ul>
                    </div>
                </div>
                ''',
                'safety_requirements': '''
                <div class="safety-grid">
                    <div class="safety-item">
                        <i class="fas fa-child"></i>
                        <h4>Idade Mínima</h4>
                        <p>12 anos (menores acompanhados)</p>
                    </div>
                    <div class="safety-item">
                        <i class="fas fa-heartbeat"></i>
                        <h4>Condições Físicas</h4>
                        <p>Boa saúde e condicionamento básico</p>
                    </div>
                    <div class="safety-item">
                        <i class="fas fa-cloud-rain"></i>
                        <h4>Condições Climáticas</h4>
                        <p>Atividade sujeita às condições do tempo</p>
                    </div>
                    <div class="safety-item">
                        <i class="fas fa-file-medical"></i>
                        <h4>Termo de Responsabilidade</h4>
                        <p>Obrigatório para todos os participantes</p>
                    </div>
                </div>
                ''',
                'description': '''
                <p>Venha conhecer a deslumbrante Cascata do Vinho, um dos pontos turísticos mais bonitos da região de Bento Gonçalves. Esta aventura combina caminhada em meio à natureza, técnicas de cachoeirismo e momentos inesquecíveis de contemplação.</p>
                <p>A cachoeira possui aproximadamente 15 metros de altura e oferece uma piscina natural perfeita para um banho revigorante. Durante o percurso, você será acompanhado por guias especializados que compartilharão conhecimentos sobre a fauna e flora local.</p>
                '''
            }
        }

        # Aplicar para todas as aventuras similar
        default_content = adventures_data['cascata-do-vinho']
        
        adventures = Adventure.objects.all()
        
        for adventure in adventures:
            adventure.what_includes = default_content['what_includes']
            adventure.what_to_bring = default_content['what_to_bring']  
            adventure.safety_requirements = default_content['safety_requirements']
            
            # Personalizar a descrição baseada no título
            if 'cascata' in adventure.title.lower():
                adventure.description = default_content['description']
            elif 'trilha' in adventure.title.lower():
                adventure.description = f'''
                <p>Explore a natureza exuberante através da {adventure.title}, uma trilha que oferece paisagens deslumbrantes e contato direto com a biodiversidade local.</p>
                <p>Durante o percurso, você descobrirá mirantes naturais, fauna silvestre e pontos de descanso estratégicos. Nossa equipe especializada garantirá uma experiência segura e educativa.</p>
                '''
            elif 'escalada' in adventure.title.lower():
                adventure.description = f'''
                <p>Desafie seus limites na {adventure.title}, uma experiência de escalada que combina adrenalina, técnica e vistas panorâmicas extraordinárias.</p>
                <p>Com equipamentos de primeira linha e instrutores certificados, você aprenderá técnicas de escalada enquanto desfruta de uma das vistas mais impressionantes da região.</p>
                '''
            else:
                adventure.description = f'''
                <p>Embarque na aventura {adventure.title} e descubra paisagens únicas em meio à natureza preservada do Rio Grande do Sul.</p>
                <p>Uma experiência cuidadosamente planejada para oferecer momentos inesquecíveis de conexão com a natureza, sempre com total segurança e acompanhamento profissional.</p>
                '''
            
            adventure.save()
            
            self.stdout.write(f"✅ Atualizado: {adventure.title}")

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 {adventures.count()} aventuras atualizadas com sucesso!')
        )
        
        self.stdout.write("\n📝 Conteúdo adicionado:")
        self.stdout.write("  • Descrições detalhadas")
        self.stdout.write("  • O que está incluído (com ícones)")
        self.stdout.write("  • O que levar (categorizado)")
        self.stdout.write("  • Requisitos de segurança") 