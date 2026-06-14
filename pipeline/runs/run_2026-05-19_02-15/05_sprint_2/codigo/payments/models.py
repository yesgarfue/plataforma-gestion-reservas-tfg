from django.db import models
from reservations.models import Reserva


class PagoPayPal(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('FALLIDO', 'Fallido'),
    ]

    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='pagos_paypal')
    transaction_id = models.CharField(max_length=255, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pago PayPal'
        verbose_name_plural = 'Pagos PayPal'

    def __str__(self):
        return f'Pago PayPal {self.id} - {self.reserva.codigo_seguimiento}'


class PagoContraReembolso(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
    ]

    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='pagos_contra_reembolso')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pago Contra Reembolso'
        verbose_name_plural = 'Pagos Contra Reembolso'

    def __str__(self):
        return f'Pago Contra Reembolso {self.id} - {self.reserva.codigo_seguimiento}'
