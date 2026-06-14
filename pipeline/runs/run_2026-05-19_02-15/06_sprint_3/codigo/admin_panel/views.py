from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User
from catalog.models import Barco, Categoria, Puerto, Fabricante
from reservations.models import Reserva, LineaReserva
from .forms import BoatForm


def admin_required(view_func):
    """Decorador para verificar que el usuario es administrador."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


class AdminDashboardView(View):
    """Panel de administración principal."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        total_barcos = Barco.objects.count()
        total_clientes = User.objects.filter(is_staff=False).count()
        total_reservas = Reserva.objects.count()
        reservas_pendientes = Reserva.objects.filter(estado='PENDIENTE_DE_PAGO').count()

        context = {
            'total_barcos': total_barcos,
            'total_clientes': total_clientes,
            'total_reservas': total_reservas,
            'reservas_pendientes': reservas_pendientes,
        }
        return render(request, 'admin_panel/dashboard.html', context)


class AdminBoatsListView(View):
    """Listado de barcos para administración."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        barcos = Barco.objects.all().select_related('categoria', 'puerto', 'fabricante')
        context = {'barcos': barcos}
        return render(request, 'admin_panel/boats_list.html', context)


class AdminBoatCreateView(View):
    """Crear un nuevo barco."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = BoatForm()
        context = {'form': form}
        return render(request, 'admin_panel/boats_form.html', context)

    def post(self, request):
        form = BoatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Barco creado correctamente.')
            return redirect('admin:boats_list')
        context = {'form': form}
        return render(request, 'admin_panel/boats_form.html', context)


class AdminBoatEditView(View):
    """Editar un barco existente."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        barco = get_object_or_404(Barco, id=id)
        form = BoatForm(instance=barco)
        context = {'form': form, 'barco': barco}
        return render(request, 'admin_panel/boats_form.html', context)

    def post(self, request, id):
        barco = get_object_or_404(Barco, id=id)
        form = BoatForm(request.POST, request.FILES, instance=barco)
        if form.is_valid():
            form.save()
            messages.success(request, 'Barco actualizado correctamente.')
            return redirect('admin:boats_list')
        context = {'form': form, 'barco': barco}
        return render(request, 'admin_panel/boats_form.html', context)


class AdminBoatDeleteView(View):
    """Eliminar un barco."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        barco = get_object_or_404(Barco, id=id)
        barco.delete()
        messages.success(request, 'Barco eliminado correctamente.')
        return redirect('admin:boats_list')


class AdminClientsListView(View):
    """Listado de clientes para administración."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        clientes = User.objects.filter(is_staff=False).prefetch_related('reservas')
        context = {'clientes': clientes}
        return render(request, 'admin_panel/clients_list.html', context)


class AdminClientDeleteView(View):
    """Eliminar un cliente."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        cliente = get_object_or_404(User, id=id, is_staff=False)
        
        # Verificar si tiene reservas pendientes
        reservas_pendientes = cliente.reservas.filter(estado='PENDIENTE_DE_PAGO').exists()
        if reservas_pendientes:
            messages.error(request, 'No se puede eliminar un cliente con reservas pendientes.')
            return redirect('admin:clients_list')
        
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('admin:clients_list')


class AdminReservationsListView(View):
    """Listado de reservas para administración."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        reservas = Reserva.objects.all().select_related('cliente').prefetch_related('lineas')
        
        # Filtro por estado
        estado = request.GET.get('estado')
        if estado:
            reservas = reservas.filter(estado=estado)
        
        context = {
            'reservas': reservas,
            'estado_filter': estado,
            'estados': Reserva.ESTADO_CHOICES,
        }
        return render(request, 'admin_panel/reservations_list.html', context)


class AdminReservationDetailView(View):
    """Detalle de una reserva para administración."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        reserva = get_object_or_404(Reserva, id=id)
        lineas = reserva.lineas.all()
        context = {
            'reserva': reserva,
            'lineas': lineas,
            'estados': Reserva.ESTADO_CHOICES,
        }
        return render(request, 'admin_panel/reservation_detail.html', context)


class AdminReservationChangeStateView(View):
    """Cambiar el estado de una reserva."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Acceso denegado. Solo administradores.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):
        reserva = get_object_or_404(Reserva, id=id)
        nuevo_estado = request.POST.get('nuevo_estado')
        
        # Validar que el nuevo estado es válido
        estados_validos = [choice[0] for choice in Reserva.ESTADO_CHOICES]
        if nuevo_estado not in estados_validos:
            messages.error(request, 'Estado inválido.')
            return redirect('admin:reservation_detail', id=id)
        
        # Validar transiciones permitidas
        transiciones_permitidas = {
            'PENDIENTE_DE_PAGO': ['PAGADO', 'PENDIENTE_DE_PAGO'],
            'PAGADO': ['EN_USO', 'PAGADO'],
            'EN_USO': ['DEVUELTO', 'EN_USO'],
            'DEVUELTO': ['DEVUELTO'],
        }
        
        if nuevo_estado not in transiciones_permitidas.get(reserva.estado, []):
            messages.error(request, f'No se puede cambiar de {reserva.estado} a {nuevo_estado}.')
            return redirect('admin:reservation_detail', id=id)
        
        reserva.estado = nuevo_estado
        reserva.save()
        messages.success(request, f'Estado de la reserva actualizado a {nuevo_estado}.')
        return redirect('admin:reservation_detail', id=id)
