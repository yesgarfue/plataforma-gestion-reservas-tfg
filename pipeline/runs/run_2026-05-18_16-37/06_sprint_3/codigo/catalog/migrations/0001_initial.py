from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Fabricante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, unique=True)),
                ('pais', models.CharField(blank=True, max_length=120)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Puerto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, unique=True)),
                ('ubicacion', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Barco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('precio_dia', models.DecimalField(decimal_places=2, max_digits=8)),
                ('capacidad', models.PositiveIntegerField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='barcos/')),
                ('descripcion', models.TextField(blank=True)),
                ('disponible', models.BooleanField(default=True)),
                ('cantidad_disponible', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.categoria')),
                ('fabricante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.fabricante')),
                ('puerto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.puerto')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
