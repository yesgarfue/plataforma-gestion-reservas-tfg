from django import forms
from catalog.models import Barco, Categoria, Puerto, Fabricante
from django.core.exceptions import ValidationError


class BoatForm(forms.ModelForm):
    class Meta:
        model = Barco
        fields = ['nombre', 'categoria', 'puerto', 'fabricante', 'precio_dia', 'capacidad', 'imagen', 'disponibilidad', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del barco'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'puerto': forms.Select(attrs={'class': 'form-select'}),
            'fabricante': forms.Select(attrs={'class': 'form-select'}),
            'precio_dia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio por día', 'step': '0.01'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidad de personas'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'disponibilidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Unidades disponibles'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_precio_dia(self):
        precio = self.cleaned_data.get('precio_dia')
        if precio is not None and precio < 0:
            raise ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad is not None and capacidad < 1:
            raise ValidationError('La capacidad debe ser al menos 1 persona.')
        return capacidad

    def clean_disponibilidad(self):
        disponibilidad = self.cleaned_data.get('disponibilidad')
        if disponibilidad is not None and disponibilidad < 0:
            raise ValidationError('La disponibilidad no puede ser negativa.')
        return disponibilidad
