from django.db import models
from django.contrib.auth.models import User
from catalog.models import Barco
import uuid


class LineaCarrito(models.Model):
    sesion_id = models.CharField(max_length=40)
    barco = models.ForeignKey(Barco, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Líneas de Carrito'

    def __str__(self):
        return f'{self.barco.nombre} - {self.sesion_id}'


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE_DE_PAGO', 'Pendiente de Pago'),
        ('PAGADO', 'Pagado'),
        ('EN_USO', 'En Uso'),
        ('DEVUELTO', 'Devuelto'),
    ]
    METODO_PAGO_CHOICES = [
        ('PAYPAL', 'PayPal'),
        ('CONTRA_REEMBOLSO', 'Contra Reembolso'),
    ]

    codigo_seguimiento = models.CharField(max_length=32, unique=True, default=uuid.uuid4)
    cliente = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    nombre_cliente = models.CharField(max_length=120)
    email_contacto = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE_DE_PAGO')
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    importe_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva {self.codigo_seguimiento}'


class LineaReserva(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    barco = models.ForeignKey(Barco, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario_dia = models.DecimalField(max_digits=8, decimal_places=2)
    tasa_combustible_dia = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = 'Líneas de Reserva'

    def __str__(self):
        return f'{self.barco.nombre} - Reserva {self.reserva.codigo_seguimiento}'


class PagoPayPal(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('FALLIDO', 'Fallido'),
    ]

    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Pagos PayPal'

    def __str__(self):
        return f'Pago {self.reserva.codigo_seguimiento}'
