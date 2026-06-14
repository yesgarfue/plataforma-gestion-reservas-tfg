from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from accounts.models import User
from catalog.models import Barco, Categoria, Puerto, Fabricante
from reservations.models import Reserva, LineaReserva
from .forms import BarcoForm

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
            
            # Estadísticas
            total_barcos = Barco.objects.count()
            total_clientes = User.objects.filter(es_administrador=False).count()
            total_reservas = Reserva.objects.count()
            reservas_pendientes = Reserva.objects.filter(estado='PENDIENTE_DE_PAGO').count()
            
            context = {
                'user': user,
                'total_barcos': total_barcos,
                'total_clientes': total_clientes,
                'total_reservas': total_reservas,
                'reservas_pendientes': reservas_pendientes,
            }
            return render(request, 'admin_panel/dashboard.html', context)
        except User.DoesNotExist:
            return redirect('accounts:login')

class AdminBoatsListView(View):
    """Vista de listado de barcos para administrador"""
    
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            barcos = Barco.objects.all().order_by('-created_at')
            return render(request, 'admin_panel/boats_list.html', {
                'user': user,
                'barcos': barcos,
            })
        except User.DoesNotExist:
            return redirect('accounts:login')

class AdminBoatsCreateView(View):
    """Vista para crear un nuevo barco"""
    
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            form = BarcoForm()
            return render(request, 'admin_panel/boats_form.html', {
                'user': user,
                'form': form,
                'titulo': 'Crear Barco',
            })
        except User.DoesNotExist:
            return redirect('accounts:login')
    
    def post(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            form = BarcoForm(request.POST, request.FILES)
            if form.is_valid():
                barco = form.save()
                messages.success(request, f'Barco "{barco.nombre}" creado exitosamente.')
                return redirect('admin_panel:boats_list')
            
            return render(request, 'admin_panel/boats_form.html', {
                'user': user,
                'form': form,
                'titulo': 'Crear Barco',
            })
        except User.DoesNotExist:
            return redirect('accounts:login')

class AdminBoatsEditView(View):
    """Vista para editar un barco existente"""
    
    def get(self, request, id):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            barco = get_object_or_404(Barco, id=id)
            form = BarcoForm(instance=barco)
            return render(request, 'admin_panel/boats_form.html', {
                'user': user,
                'form': form,
                'barco': barco,
                'titulo': f'Editar Barco: {barco.nombre}',
            })
        except User.DoesNotExist:
            return redirect('accounts:login')
    
    def post(self, request, id):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            barco = get_object_or_404(Barco, id=id)
            form = BarcoForm(request.POST, request.FILES, instance=barco)
            if form.is_valid():
                barco = form.save()
                messages.success(request, f'Barco "{barco.nombre}" actualizado exitosamente.')
                return redirect('admin_panel:boats_list')
            
            return render(request, 'admin_panel/boats_form.html', {
                'user': user,
                'form': form,
                'barco': barco,
                'titulo': f'Editar Barco: {barco.nombre}',
            })
        except User.DoesNotExist:
            return redirect('accounts:login')

class AdminBoatsDeleteView(View):
    """Vista para eliminar un barco"""
    
    def post(self, request, id):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            barco = get_object_or_404(Barco, id=id)
            nombre_barco = barco.nombre
            barco.delete()
            messages.success(request, f'Barco "{nombre_barco}" eliminado exitosamente.')
        except User.DoesNotExist:
            return redirect('accounts:login')
        
        return redirect('admin_panel:boats_list')

class AdminClientsListView(View):
    """Vista de listado de clientes para administrador"""
    
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            clientes = User.objects.filter(es_administrador=False).order_by('-created_at')
            
            # Obtener información de reservas para cada cliente
            clientes_info = []
            for cliente in clientes:
                reservas = Reserva.objects.filter(cliente=cliente)
                reservas_pendientes = reservas.filter(estado='PENDIENTE_DE_PAGO').count()
                clientes_info.append({
                    'cliente': cliente,
                    'total_reservas': reservas.count(),
                    'reservas_pendientes': reservas_pendientes,
                    'puede_eliminar': reservas_pendientes == 0,
                })
            
            return render(request, 'admin_panel/clients_list.html', {
                'user': user,
                'clientes_info': clientes_info,
            })
        except User.DoesNotExist:
            return redirect('accounts:login')

class AdminClientsDeleteView(View):
    """Vista para eliminar un cliente"""
    
    def post(self, request, id):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            cliente = get_object_or_404(User, id=id)
            
            # Verificar si el cliente tiene reservas pendientes
            reservas_pendientes = Reserva.objects.filter(cliente=cliente, estado='PENDIENTE_DE_PAGO').count()
            if reservas_pendientes > 0:
                messages.error(request, f'No se puede eliminar el cliente porque tiene {reservas_pendientes} reserva(s) pendiente(s) de pago.')
                return redirect('admin_panel:clients_list')
            
            email_cliente = cliente.email
            cliente.delete()
            messages.success(request, f'Cliente "{email_cliente}" eliminado exitosamente.')
        except User.DoesNotExist:
            return redirect('accounts:login')
        
        return redirect('admin_panel:clients_list')

class AdminReservationsListView(View):
    """Vista de listado de reservas para administrador"""
    
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            # Filtrar por estado si se proporciona
            estado = request.GET.get('estado')
            if estado:
                reservas = Reserva.objects.filter(estado=estado).order_by('-created_at')
            else:
                reservas = Reserva.objects.all().order_by('-created_at')
            
            return render(request, 'admin_panel/reservations_list.html', {
                'user': user,
                'reservas': reservas,
                'estado_filtro': estado,
            })
        except User.DoesNotExist:
            return redirect('accounts:login')

class AdminReservationsDetailView(View):
    """Vista de detalle de una reserva"""
    
    def get(self, request, id):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            reserva = get_object_or_404(Reserva, id=id)
            lineas = reserva.lineas.all()
            
            # Determinar transiciones disponibles
            transiciones_disponibles = []
            if reserva.estado == 'PENDIENTE_DE_PAGO':
                transiciones_disponibles = ['PAGADO', 'CANCELADA']
            elif reserva.estado == 'PAGADO':
                transiciones_disponibles = ['EN_USO', 'CANCELADA']
            elif reserva.estado == 'EN_USO':
                transiciones_disponibles = ['DEVUELTO']
            
            return render(request, 'admin_panel/reservations_detail.html', {
                'user': user,
                'reserva': reserva,
                'lineas': lineas,
                'transiciones_disponibles': transiciones_disponibles,
            })
        except User.DoesNotExist:
            return redirect('accounts:login')

class AdminReservationsChangeStateView(View):
    """Vista para cambiar el estado de una reserva"""
    
    def post(self, request, id):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            if not user.es_administrador:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                return redirect('core:home')
            
            reserva = get_object_or_404(Reserva, id=id)
            nuevo_estado = request.POST.get('nuevo_estado')
            
            # Validar transición
            transiciones_validas = {
                'PENDIENTE_DE_PAGO': ['PAGADO', 'CANCELADA'],
                'PAGADO': ['EN_USO', 'CANCELADA'],
                'EN_USO': ['DEVUELTO'],
                'DEVUELTO': [],
                'CANCELADA': [],
            }
            
            if nuevo_estado not in transiciones_validas.get(reserva.estado, []):
                messages.error(request, 'Transición de estado no válida.')
                return redirect('admin_panel:reservations_detail', id=id)
            
            reserva.estado = nuevo_estado
            reserva.save()
            messages.success(request, f'Estado de la reserva actualizado a {reserva.get_estado_display()}.')
        except User.DoesNotExist:
            return redirect('accounts:login')
        
        return redirect('admin_panel:reservations_detail', id=id)
