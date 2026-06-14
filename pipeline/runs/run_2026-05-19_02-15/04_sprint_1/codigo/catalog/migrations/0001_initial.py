from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, unique=True)),
                ('descripcion', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
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
                'verbose_name': 'Fabricante',
                'verbose_name_plural': 'Fabricantes',
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
                'verbose_name': 'Puerto',
                'verbose_name_plural': 'Puertos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Barco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('precio_dia', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('capacidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='barcos/')),
                ('disponibilidad', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('activo', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='barcos', to='catalog.categoria')),
                ('fabricante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='barcos', to='catalog.fabricante')),
                ('puerto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='barcos', to='catalog.puerto')),
            ],
            options={
                'verbose_name': 'Barco',
                'verbose_name_plural': 'Barcos',
                'ordering': ['nombre'],
            },
        ),
    ]
