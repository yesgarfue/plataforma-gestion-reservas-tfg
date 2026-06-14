from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class CashOnDeliveryService:
    """
    Servicio para pagos contra reembolso.
    """

    @staticmethod
    def procesar_pago(reserva):
        """
        Procesa un pago contra reembolso.
        Marca la reserva como pagada y envía confirmación.
        """
        try:
            reserva.estado = 'PAGADO'
            reserva.save()

            # Enviar correo de confirmación
            asunto = f'Pago Confirmado - Código: {reserva.codigo_seguimiento}'
            contexto = {
                'reserva': reserva,
                'lineas': reserva.lineas.all(),
                'metodo_pago': 'Contra Reembolso',
            }
            mensaje_html = render_to_string('payments/email_pago_confirmado.html', contexto)
            send_mail(
                asunto,
                f'Tu pago ha sido confirmado. Código: {reserva.codigo_seguimiento}',
                settings.DEFAULT_FROM_EMAIL,
                [reserva.email_contacto],
                html_message=mensaje_html,
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f'Error al procesar pago contra reembolso: {e}')
            return False
