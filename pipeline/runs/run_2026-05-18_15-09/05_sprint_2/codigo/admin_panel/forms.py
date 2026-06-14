from django import forms
from catalog.models import Barco, Categoria, Puerto, Fabricante


class BarcoForm(forms.ModelForm):
    class Meta:
        model = Barco
        fields = ['nombre', 'categoria', 'puerto', 'fabricante', 'precio_dia', 'capacidad', 'imagen', 'descripcion', 'disponible']
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
        }
