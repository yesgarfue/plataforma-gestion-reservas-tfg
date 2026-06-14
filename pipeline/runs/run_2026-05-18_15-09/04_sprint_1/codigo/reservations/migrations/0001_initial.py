from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LineaCarrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sesion_id', models.CharField(max_length=40)),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('barco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.barco')),
            ],
            options={
                'verbose_name_plural': 'Líneas de Carrito',
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_seguimiento', models.CharField(default=uuid.uuid4, max_length=32, unique=True)),
                ('nombre_cliente', models.CharField(max_length=120)),
                ('email_contacto', models.EmailField(max_length=254)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('estado', models.CharField(choices=[('PENDIENTE_DE_PAGO', 'Pendiente de Pago'), ('PAGADO', 'Pagado'), ('EN_USO', 'En Uso'), ('DEVUELTO', 'Devuelto')], default='PENDIENTE_DE_PAGO', max_length=20)),
                ('metodo_pago', models.CharField(choices=[('PAYPAL', 'PayPal'), ('CONTRA_REEMBOLSO', 'Contra Reembolso')], max_length=20)),
                ('importe_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reservas',
            },
        ),
        migrations.CreateModel(
            name='PagoPayPal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('COMPLETADO', 'Completado'), ('FALLIDO', 'Fallido')], default='PENDIENTE', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.reserva')),
            ],
            options={
                'verbose_name_plural': 'Pagos PayPal',
            },
        ),
        migrations.CreateModel(
            name='LineaReserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario_dia', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tasa_combustible_dia', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('barco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.barco')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.reserva')),
            ],
            options={
                'verbose_name_plural': 'Líneas de Reserva',
            },
        ),
    ]
