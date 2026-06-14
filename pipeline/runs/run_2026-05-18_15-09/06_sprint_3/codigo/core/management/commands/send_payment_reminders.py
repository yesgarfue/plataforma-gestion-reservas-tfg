from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from reservations.models import Reserva


class Command(BaseCommand):
    help = 'Envía recordatorios de pago pendiente a clientes'

    def handle(self, *args, **options):
        # Obtener la fecha de mañana
        manana = timezone.now().date() + timedelta(days=1)
        
        # Buscar reservas que comienzan mañana y están pendientes de pago
        reservas = Reserva.objects.filter(
            fecha_inicio=manana,
            estado='PENDIENTE_DE_PAGO'
        )
        
        for reserva in reservas:
            self._enviar_recordatorio(reserva)
        
        self.stdout.write(self.style.SUCCESS(f'Se enviaron {reservas.count()} recordatorios de pago.'))
    
    def _enviar_recordatorio(self, reserva):
        """Envía correo de recordatorio de pago pendiente."""
        try:
            asunto = f'Recordatorio: Pago Pendiente - Reserva {reserva.codigo_seguimiento}'
            mensaje = f"""Estimado/a {reserva.nombre_cliente},

Le recordamos que su reserva comienza mañana y aún tiene un pago pendiente.

Detalles de su reserva:
- Código de Seguimiento: {reserva.codigo_seguimiento}
- Fechas: {reserva.fecha_inicio.strftime('%d/%m/%Y')} a {reserva.fecha_fin.strftime('%d/%m/%Y')}
- Importe Total: {reserva.importe_total}€
- Método de Pago: {reserva.get_metodo_pago_display()}

Por favor, complete el pago lo antes posible para confirmar su reserva.

Si ya ha realizado el pago, ignore este mensaje.

Saludos,
El equipo de Hundidos"""
            
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [reserva.email_contacto],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error al enviar recordatorio: {e}")
