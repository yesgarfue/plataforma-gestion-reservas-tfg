from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservations.models import Reserva
from reservations.services.email import EmailService

class Command(BaseCommand):
    help = 'Envía recordatorios de pago para reservas pendientes'

    def handle(self, *args, **options):
        # Obtener reservas pendientes de pago creadas hace más de 24 horas
        hace_24_horas = timezone.now() - timedelta(hours=24)
        reservas_pendientes = Reserva.objects.filter(
            estado='PENDIENTE_DE_PAGO',
            created_at__lt=hace_24_horas
        )
        
        for reserva in reservas_pendientes:
            if EmailService.send_payment_reminder(reserva):
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Recordatorio enviado para reserva {reserva.codigo_seguimiento}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error al enviar recordatorio para reserva {reserva.codigo_seguimiento}'
                    )
                )
