from django.db import models
from django.contrib.auth.models import User
from catalog.models import Barco
from django.core.validators import MinValueValidator
import uuid


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
    cliente = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reservas')
    email_contacto = models.EmailField()
    nombre_cliente = models.CharField(max_length=120)
    apellido_cliente = models.CharField(max_length=120)
    telefono_cliente = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE_DE_PAGO')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    importe_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    recordatorio_enviado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Reserva {self.codigo_seguimiento}'


class LineaReserva(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='lineas')
    barco = models.ForeignKey(Barco, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario_dia = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    tasa_combustible_dia = models.DecimalField(max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Línea de Reserva'
        verbose_name_plural = 'Líneas de Reserva'

    def __str__(self):
        return f'{self.barco.nombre} x {self.cantidad}'
