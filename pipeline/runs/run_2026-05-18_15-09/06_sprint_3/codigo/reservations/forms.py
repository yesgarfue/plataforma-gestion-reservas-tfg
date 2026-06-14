from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta


class AgregarCarritoForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')
    fecha_inicio = forms.DateField(label='Fecha de Inicio', widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(label='Fecha de Fin', widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_inicio < date.today():
                raise ValidationError('La fecha de inicio no puede ser anterior a hoy.')
            if fecha_fin <= fecha_inicio:
                raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
        return cleaned_data


class DatosClienteForm(forms.Form):
    nombre_cliente = forms.CharField(max_length=120, label='Nombre Completo')
    email_contacto = forms.EmailField(label='Correo Electrónico')
    telefono = forms.CharField(max_length=20, label='Teléfono', required=False)


class MetodoPagoForm(forms.Form):
    METODO_CHOICES = [
        ('PAYPAL', 'PayPal'),
        ('CONTRA_REEMBOLSO', 'Contra Reembolso'),
    ]
    metodo_pago = forms.ChoiceField(choices=METODO_CHOICES, label='Método de Pago', widget=forms.RadioSelect)
