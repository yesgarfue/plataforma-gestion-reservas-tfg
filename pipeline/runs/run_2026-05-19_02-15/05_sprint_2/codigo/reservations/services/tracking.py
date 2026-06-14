import uuid
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta


class TrackingService:
    @staticmethod
    def generar_codigo_seguimiento():
        """
        Genera un código de seguimiento único.
        """
        return str(uuid.uuid4())[:8].upper()

    @staticmethod
    def enviar_confirmacion_reserva(reserva):
        """
        Envía un correo de confirmación de reserva al cliente.
        """
        try:
            asunto = f'Confirmación de Reserva - Código: {reserva.codigo_seguimiento}'
            contexto = {
                'reserva': reserva,
                'lineas': reserva.lineas.all(),
                'fecha_inicio': reserva.fecha_inicio,
                'fecha_fin': reserva.fecha_fin,
                'importe_total': reserva.importe_total,
            }
            mensaje_html = render_to_string('reservations/email_confirmacion.html', contexto)
            send_mail(
                asunto,
                f'Tu reserva ha sido confirmada. Código de seguimiento: {reserva.codigo_seguimiento}',
                settings.DEFAULT_FROM_EMAIL,
                [reserva.email_contacto],
                html_message=mensaje_html,
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f'Error al enviar correo de confirmación: {e}')
            return False

    @staticmethod
    def enviar_recordatorio_pago(reserva):
        """
        Envía un correo de recordatorio de pago pendiente.
        Se envía cuando falta un día para el inicio y sigue en PENDIENTE_DE_PAGO.
        """
        try:
            asunto = f'Recordatorio: Pago Pendiente - Código: {reserva.codigo_seguimiento}'
            contexto = {
                'reserva': reserva,
                'lineas': reserva.lineas.all(),
                'fecha_inicio': reserva.fecha_inicio,
                'importe_total': reserva.importe_total,
            }
            mensaje_html = render_to_string('reservations/email_recordatorio.html', contexto)
            send_mail(
                asunto,
                f'Tu reserva tiene un pago pendiente. Código: {reserva.codigo_seguimiento}',
                settings.DEFAULT_FROM_EMAIL,
                [reserva.email_contacto],
                html_message=mensaje_html,
                fail_silently=False,
            )
            reserva.recordatorio_enviado = True
            reserva.save()
            return True
        except Exception as e:
            print(f'Error al enviar recordatorio: {e}')
            return False

    @staticmethod
    def debe_enviar_recordatorio(reserva):
        """
        Determina si debe enviarse un recordatorio de pago.
        Condiciones:
        - Estado es PENDIENTE_DE_PAGO
        - Falta exactamente 1 día para el inicio
        - No se ha enviado recordatorio aún
        """
        from datetime import date
        if reserva.estado != 'PENDIENTE_DE_PAGO':
            return False
        if reserva.recordatorio_enviado:
            return False
        dias_hasta_inicio = (reserva.fecha_inicio - date.today()).days
        return dias_hasta_inicio == 1
