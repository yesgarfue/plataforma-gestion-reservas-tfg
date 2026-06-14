from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('catalog', '0001_initial'),
        ('accounts', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_seguimiento', models.CharField(max_length=32, unique=True)),
                ('estado', models.CharField(choices=[('PENDIENTE_DE_PAGO', 'Pendiente de pago'), ('PAGADO', 'Pagado'), ('EN_USO', 'En uso'), ('DEVUELTO', 'Devuelto')], default='PENDIENTE_DE_PAGO', max_length=20)),
                ('nombre_cliente', models.CharField(max_length=120)),
                ('email_cliente', models.EmailField(max_length=254)),
                ('telefono_cliente', models.CharField(blank=True, max_length=20)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('metodo_pago', models.CharField(choices=[('PAYPAL', 'PayPal'), ('CONTRA_REEMBOLSO', 'Contra-reembolso')], max_length=20)),
                ('importe_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tasa_combustible', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='LineaReserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario_dia', models.DecimalField(decimal_places=2, max_digits=8)),
                ('barco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.barco')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineas', to='reservations.reserva')),
            ],
        ),
    ]
