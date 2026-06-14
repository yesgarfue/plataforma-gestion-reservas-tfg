from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_seguimiento', models.CharField(default=uuid.uuid4, max_length=32, unique=True)),
                ('email_contacto', models.EmailField(max_length=254)),
                ('nombre_cliente', models.CharField(max_length=120)),
                ('apellido_cliente', models.CharField(max_length=120)),
                ('telefono_cliente', models.CharField(blank=True, max_length=20)),
                ('estado', models.CharField(choices=[('PENDIENTE_DE_PAGO', 'Pendiente de Pago'), ('PAGADO', 'Pagado'), ('EN_USO', 'En Uso'), ('DEVUELTO', 'Devuelto')], default='PENDIENTE_DE_PAGO', max_length=20)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('importe_total', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('metodo_pago', models.CharField(choices=[('PAYPAL', 'PayPal'), ('CONTRA_REEMBOLSO', 'Contra Reembolso')], max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('recordatorio_enviado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='LineaReserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('precio_unitario_dia', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('tasa_combustible_dia', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('barco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.barco')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineas', to='reservations.reserva')),
            ],
            options={
                'verbose_name': 'Línea de Reserva',
                'verbose_name_plural': 'Líneas de Reserva',
            },
        ),
    ]
