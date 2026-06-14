from django.db import models
from catalog.models import Barco
from accounts.models import User

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE_DE_PAGO', 'Pendiente de pago'),
        ('PAGADO', 'Pagado'),
        ('EN_USO', 'En uso'),
        ('DEVUELTO', 'Devuelto'),
    ]
    METODO_PAGO_CHOICES = [
        ('PAYPAL', 'PayPal'),
        ('CONTRA_REEMBOLSO', 'Contra-reembolso'),
    ]

    codigo_seguimiento = models.CharField(max_length=32, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE_DE_PAGO')
    cliente = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    nombre_cliente = models.CharField(max_length=120)
    email_cliente = models.EmailField()
    telefono_cliente = models.CharField(max_length=20, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    importe_total = models.DecimalField(max_digits=10, decimal_places=2)
    tasa_combustible = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Reserva {self.codigo_seguimiento}'

    class Meta:
        ordering = ['-created_at']

class LineaReserva(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='lineas')
    barco = models.ForeignKey(Barco, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario_dia = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.barco.nombre} x {self.cantidad}'
