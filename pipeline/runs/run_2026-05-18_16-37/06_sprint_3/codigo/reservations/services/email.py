from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class EmailService:
    """Servicio para envío de correos electrónicos"""
    
    @staticmethod
    def send_reservation_confirmation(reserva):
        """Envía un correo de confirmación de reserva"""
        subject = f'Confirmación de reserva - Código: {reserva.codigo_seguimiento}'
        
        context = {
            'reserva': reserva,
            'lineas': reserva.lineas.all(),
        }
        
        html_message = render_to_string('reservations/email_confirmation.html', context)
        
        try:
            send_mail(
                subject,
                f'Tu reserva ha sido confirmada. Código de seguimiento: {reserva.codigo_seguimiento}',
                settings.DEFAULT_FROM_EMAIL or 'noreply@hundidos.com',
                [reserva.email_cliente],
                html_message=html_message,
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f'Error al enviar correo: {str(e)}')
            return False
    
    @staticmethod
    def send_payment_reminder(reserva):
        """Envía un recordatorio de pago pendiente"""
        subject = f'Recordatorio de pago - Reserva {reserva.codigo_seguimiento}'
        
        context = {
            'reserva': reserva,
        }
        
        html_message = render_to_string('reservations/email_reminder.html', context)
        
        try:
            send_mail(
                subject,
                f'Tu reserva {reserva.codigo_seguimiento} está pendiente de pago.',
                settings.DEFAULT_FROM_EMAIL or 'noreply@hundidos.com',
                [reserva.email_cliente],
                html_message=html_message,
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f'Error al enviar correo: {str(e)}')
            return False
