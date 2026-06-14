from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Puerto(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    ubicacion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Fabricante(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    pais = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Barco(models.Model):
    nombre = models.CharField(max_length=120)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    puerto = models.ForeignKey(Puerto, on_delete=models.PROTECT)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.PROTECT)
    precio_dia = models.DecimalField(max_digits=8, decimal_places=2)
    capacidad = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='barcos/', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)
    cantidad_disponible = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['-created_at']
