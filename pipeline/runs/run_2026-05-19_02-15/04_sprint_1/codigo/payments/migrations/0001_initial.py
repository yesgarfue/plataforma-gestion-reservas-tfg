from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoPayPal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=255)),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('COMPLETADO', 'Completado'), ('FALLIDO', 'Fallido')], default='PENDIENTE', max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos_paypal', to='reservations.reserva')),
            ],
            options={
                'verbose_name': 'Pago PayPal',
                'verbose_name_plural': 'Pagos PayPal',
            },
        ),
        migrations.CreateModel(
            name='PagoContraReembolso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('PAGADO', 'Pagado')], default='PENDIENTE', max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos_contra_reembolso', to='reservations.reserva')),
            ],
            options={
                'verbose_name': 'Pago Contra Reembolso',
                'verbose_name_plural': 'Pagos Contra Reembolso',
            },
        ),
    ]
