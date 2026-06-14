from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
import re


class ReservationStep1Form(forms.Form):
    fecha_inicio = forms.DateField(
        label='Fecha de Inicio',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        help_text='Selecciona la fecha de inicio del alquiler'
    )
    fecha_fin = forms.DateField(
        label='Fecha de Fin',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        help_text='Selecciona la fecha de fin del alquiler'
    )

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


class ReservationStep2Form(forms.Form):
    nombre_cliente = forms.CharField(
        label='Nombre',
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    apellido_cliente = forms.CharField(
        label='Apellido',
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    email_contacto = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    telefono_cliente = forms.CharField(
        label='Teléfono',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+34 600 000 000'
        })
    )

    def clean_nombre_cliente(self):
        nombre = self.cleaned_data.get('nombre_cliente')
        if nombre and len(nombre.strip()) == 0:
            raise ValidationError('El nombre no puede estar vacío.')
        return nombre

    def clean_apellido_cliente(self):
        apellido = self.cleaned_data.get('apellido_cliente')
        if apellido and len(apellido.strip()) == 0:
            raise ValidationError('El apellido no puede estar vacío.')
        return apellido

    def clean_telefono_cliente(self):
        telefono = self.cleaned_data.get('telefono_cliente')
        if telefono:
            if not re.match(r'^[\d\s\+\-\(\)]{7,20}$', telefono):
                raise ValidationError('El teléfono no tiene un formato válido.')
        return telefono


class ReservationStep3Form(forms.Form):
    METODO_PAGO_CHOICES = [
        ('PAYPAL', 'PayPal'),
        ('CONTRA_REEMBOLSO', 'Contra Reembolso'),
    ]

    metodo_pago = forms.ChoiceField(
        label='Método de Pago',
        choices=METODO_PAGO_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )
    terminos = forms.BooleanField(
        label='Acepto los términos y condiciones',
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )

    def clean_terminos(self):
        terminos = self.cleaned_data.get('terminos')
        if not terminos:
            raise ValidationError('Debes aceptar los términos y condiciones para continuar.')
        return terminos
