from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from accounts.models import User

class AdminDashboardView(View):
    """Vista del panel de administración"""
    
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder al panel de administración.')
                return redirect('core:home')
            
            return render(request, 'admin_panel/dashboard.html', {'user': user})
        except User.DoesNotExist:
            return redirect('accounts:login')
