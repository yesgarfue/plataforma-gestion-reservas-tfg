from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import User
from .forms import RegisterForm, LoginForm
from reservations.models import Reserva

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            messages.success(request, 'Registro exitoso. Bienvenido.')
            return redirect('core:home')
        return render(request, 'accounts/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    messages.success(request, 'Inicio de sesión exitoso.')
                    return redirect('core:home')
                else:
                    messages.error(request, 'Correo o contraseña incorrectos.')
            except User.DoesNotExist:
                messages.error(request, 'Correo o contraseña incorrectos.')
        return render(request, 'accounts/login.html', {'form': form})

class LogoutView(View):
    def post(self, request):
        if 'user_id' in request.session:
            del request.session['user_id']
        messages.success(request, 'Sesión cerrada correctamente.')
        return redirect('core:home')

@method_decorator(login_required(login_url='accounts:login'), name='dispatch')
class ProfileView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        try:
            user = User.objects.get(id=user_id)
            reservas = Reserva.objects.filter(cliente_id=user_id).order_by('-created_at')
            return render(request, 'accounts/profile.html', {
                'user': user,
                'reservas': reservas
            })
        except User.DoesNotExist:
            return redirect('accounts:login')
