from django import forms
from catalog.models import Barco, Categoria, Puerto, Fabricante
from django.core.exceptions import ValidationError

class BarcoForm(forms.ModelForm):
    class Meta:
        model = Barco
        fields = ['nombre', 'categoria', 'puerto', 'fabricante', 'precio_dia', 'capacidad', 'imagen', 'descripcion', 'disponible', 'cantidad_disponible']
        labels = {
            'nombre': 'Nombre del barco',
            'categoria': 'Categoría',
            'puerto': 'Puerto',
            'fabricante': 'Fabricante',
            'precio_dia': 'Precio por día (€)',
            'capacidad': 'Capacidad (personas)',
            'imagen': 'Imagen',
            'descripcion': 'Descripción',
            'disponible': 'Disponible',
            'cantidad_disponible': 'Cantidad disponible',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'puerto': forms.Select(attrs={'class': 'form-control'}),
            'fabricante': forms.Select(attrs={'class': 'form-control'}),
            'precio_dia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_precio_dia(self):
        precio = self.cleaned_data.get('precio_dia')
        if precio and precio <= 0:
            raise ValidationError('El precio debe ser mayor a 0.')
        return precio

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad and capacidad <= 0:
            raise ValidationError('La capacidad debe ser mayor a 0.')
        return capacidad

    def clean_cantidad_disponible(self):
        cantidad = self.cleaned_data.get('cantidad_disponible')
        if cantidad and cantidad <= 0:
            raise ValidationError('La cantidad disponible debe ser mayor a 0.')
        return cantidad
