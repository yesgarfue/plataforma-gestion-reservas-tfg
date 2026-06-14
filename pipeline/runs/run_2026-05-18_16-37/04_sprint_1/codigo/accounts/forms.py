from django import forms
from django.core.exceptions import ValidationError
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Contraseña',
        min_length=6
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirmar contraseña',
        min_length=6
    )

    class Meta:
        model = User
        fields = ['email', 'nombre', 'telefono']
        labels = {
            'email': 'Correo electrónico',
            'nombre': 'Nombre',
            'telefono': 'Teléfono',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Contraseña'
    )
