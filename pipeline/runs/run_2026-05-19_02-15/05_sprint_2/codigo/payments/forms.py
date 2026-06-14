from django import forms
from django.core.exceptions import ValidationError


class PayPalPaymentForm(forms.Form):
    """
    Formulario para procesar pagos con PayPal.
    """
    pass


class CashOnDeliveryForm(forms.Form):
    """
    Formulario para pagos contra reembolso.
    """
    aceptar_terminos = forms.BooleanField(
        label='Acepto los términos de pago contra reembolso',
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )

    def clean_aceptar_terminos(self):
        aceptar = self.cleaned_data.get('aceptar_terminos')
        if not aceptar:
            raise ValidationError('Debes aceptar los términos para continuar.')
        return aceptar
