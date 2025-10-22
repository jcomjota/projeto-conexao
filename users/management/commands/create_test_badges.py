from django.core.management.base import BaseCommand
from users.models import Badge, Reward


class Command(BaseCommand):
    help = 'Cria insígnias e recompensas iniciais para teste'

    def handle(self, *args, **kwargs):
        # Criar insígnias
        badges = [
            {
                'name': 'Primeira Aventura',
                'description': 'Completou sua primeira aventura',
                'icon': 'lucide-flag',
                'points': 10,
                'requirement_type': 'adventures_completed',
                'requirement_value': {'count': 1}
            },
            {
                'name': 'Aventureiro Dedicado',
                'description': 'Completou 5 aventuras',
                'icon': 'lucide-mountain',
                'points': 25,
                'requirement_type': 'adventures_completed',
                'requirement_value': {'count': 5}
            },
            {
                'name': 'Mestre das Trilhas',
                'description': 'Completou 10 aventuras',
                'icon': 'lucide-map',
                'points': 50,
                'requirement_type': 'adventures_completed',
                'requirement_value': {'count': 10}
            },
            {
                'name': 'Colecionador de Pontos',
                'description': 'Acumulou 100 pontos',
                'icon': 'lucide-star',
                'points': 20,
                'requirement_type': 'points_earned',
                'requirement_value': {'points': 100}
            },
            {
                'name': 'Aventureiro Premium',
                'description': 'Realizou pagamento via PIX',
                'icon': 'lucide-credit-card',
                'points': 15,
                'requirement_type': 'payment_method',
                'requirement_value': {'method': 'pix'}
            }
        ]

        for badge_data in badges:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Insígnia criada: {badge.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Insígnia já existe: {badge.name}')
                )

        # Criar recompensas
        rewards = [
            {
                'name': 'Desconto de 10%',
                'description': 'Ganhe 10% de desconto na próxima aventura',
                'icon': 'lucide-percent',
                'points_cost': 100,
                'reward_type': 'discount',
                'value': {'percentage': 10}
            },
            {
                'name': 'Aventura Grátis',
                'description': 'Ganhe uma aventura gratuita à sua escolha',
                'icon': 'lucide-gift',
                'points_cost': 500,
                'reward_type': 'free_adventure',
                'value': {'limit_value': 200}
            },
            {
                'name': 'Camiseta Exclusiva',
                'description': 'Camiseta personalizada Conexão Adventure',
                'icon': 'lucide-shirt',
                'points_cost': 200,
                'reward_type': 'merchandise',
                'value': {'item': 'camiseta'}
            }
        ]

        for reward_data in rewards:
            reward, created = Reward.objects.get_or_create(
                name=reward_data['name'],
                defaults=reward_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Recompensa criada: {reward.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Recompensa já existe: {reward.name}')
                ) 