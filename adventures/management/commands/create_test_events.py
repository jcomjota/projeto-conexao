from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, time
from adventures.models import Adventure
from bookings.models import AdventureEvent


class Command(BaseCommand):
    help = 'Cria eventos de teste para as aventuras existentes'

    def handle(self, *args, **options):
        adventures = Adventure.objects.all()
        
        if not adventures.exists():
            self.stdout.write(
                self.style.ERROR('Nenhuma aventura encontrada. Execute create_test_adventures primeiro.')
            )
            return

        events_created = 0
        
        for adventure in adventures:
            # Criar 3 eventos futuros para cada aventura
            base_date = timezone.now().date() + timedelta(days=7)  # Começar em 1 semana
            
            for i in range(3):
                event_date = base_date + timedelta(days=i*14)  # A cada 2 semanas
                
                # Horários diferentes para cada aventura
                start_times = [time(8, 0), time(9, 0), time(10, 0)]
                start_time = start_times[i % len(start_times)]
                
                # Calcular horário de término baseado na duração da aventura
                end_hour = start_time.hour + adventure.duration_hours
                end_time = time(min(end_hour, 23), 0)
                
                event = AdventureEvent.objects.create(
                    adventure=adventure,
                    date=event_date,
                    start_time=start_time,
                    end_time=end_time,
                    max_participants=adventure.max_participants,
                    current_participants=0,
                    status='scheduled',
                    is_active=True,
                    meeting_instructions=f"Encontro no {adventure.meeting_point}",
                    special_notes=f"Evento {i+1} da aventura {adventure.title}"
                )
                
                events_created += 1
                self.stdout.write(
                    f"Criado evento: {adventure.title} - {event_date.strftime('%d/%m/%Y')} às {start_time.strftime('%H:%M')}"
                )

        self.stdout.write(
            self.style.SUCCESS(f'✅ {events_created} eventos criados com sucesso!')
        )
        
        # Mostrar estatísticas
        self.stdout.write("\n📊 Estatísticas:")
        for adventure in adventures:
            event_count = adventure.events.count()
            next_event = adventure.next_event
            next_event_info = f" - Próximo: {next_event.date.strftime('%d/%m/%Y')}" if next_event else " - Nenhum evento futuro"
            self.stdout.write(f"  • {adventure.title}: {event_count} eventos{next_event_info}") 