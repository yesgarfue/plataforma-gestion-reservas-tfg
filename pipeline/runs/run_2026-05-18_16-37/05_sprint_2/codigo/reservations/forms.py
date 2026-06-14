from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Reserva

class ReservationStep1Form(forms.Form):
    """Formulario para el paso 1: selección de fechas y datos del cliente"""
    fecha_inicio = forms.DateField(
        label='Fecha de inicio',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Selecciona la fecha de inicio del alquiler'
    )
    fecha_fin = forms.DateField(
        label='Fecha de fin',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Selecciona la fecha de fin del alquiler'
    )
    nombre_cliente = forms.CharField(
        label='Nombre completo',
        max_length=120,
        required=True
    )
    email_cliente = forms.EmailField(
        label='Correo electrónico',
        required=True
    )
    telefono_cliente = forms.CharField(
        label='Teléfono',
        max_length=20,
        required=False
    )

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        if fecha_inicio and fecha_inicio < date.today():
            raise ValidationError('La fecha de inicio no puede ser anterior a hoy.')
        return fecha_inicio

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
        
        return cleaned_data

class ReservationStep2Form(forms.Form):
    """Formulario para el paso 2: selección del método de pago"""
    METODO_PAGO_CHOICES = [
        ('PAYPAL', 'PayPal Sandbox'),
        ('CONTRA_REEMBOLSO', 'Contra-reembolso'),
    ]
    
    metodo_pago = forms.ChoiceField(
        label='Método de pago',
        choices=METODO_PAGO_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

class ReservationStep3Form(forms.Form):
    """Formulario para el paso 3: confirmación de la reserva"""
    aceptar_terminos = forms.BooleanField(
        label='Acepto los términos y condiciones',
        required=True
    )
