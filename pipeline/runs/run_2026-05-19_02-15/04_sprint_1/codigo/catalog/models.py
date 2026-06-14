from django.db import models
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Puerto(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    ubicacion = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Puerto'
        verbose_name_plural = 'Puertos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Fabricante(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    pais = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = 'Fabricante'
        verbose_name_plural = 'Fabricantes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Barco(models.Model):
    nombre = models.CharField(max_length=120)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='barcos')
    puerto = models.ForeignKey(Puerto, on_delete=models.PROTECT, related_name='barcos')
    fabricante = models.ForeignKey(Fabricante, on_delete=models.PROTECT, related_name='barcos')
    precio_dia = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    capacidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    imagen = models.ImageField(upload_to='barcos/', blank=True, null=True)
    disponibilidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Barco'
        verbose_name_plural = 'Barcos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
