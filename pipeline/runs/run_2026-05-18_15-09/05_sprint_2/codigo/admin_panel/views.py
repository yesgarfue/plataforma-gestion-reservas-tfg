from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from catalog.models import Barco, Categoria, Puerto, Fabricante
from reservations.models import Reserva, LineaReserva
from .forms import BarcoForm


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario es administrador."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_panel/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_barcos'] = Barco.objects.count()
        context['total_clientes'] = User.objects.filter(is_staff=False).count()
        context['total_reservas'] = Reserva.objects.count()
        context['reservas_pendientes'] = Reserva.objects.filter(estado='PENDIENTE_DE_PAGO').count()
        return context


class AdminBoatsListView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_panel/boats_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['barcos'] = Barco.objects.all().order_by('nombre')
        return context


class AdminBoatCreateView(AdminRequiredMixin, View):
    template_name = 'admin_panel/boat_form.html'
    
    def get(self, request):
        form = BarcoForm()
        return render(request, self.template_name, {'form': form, 'titulo': 'Crear Barco'})
    
    def post(self, request):
        form = BarcoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Barco creado exitosamente.')
            return redirect('admin_panel:boats_list')
        return render(request, self.template_name, {'form': form, 'titulo': 'Crear Barco'})


class AdminBoatEditView(AdminRequiredMixin, View):
    template_name = 'admin_panel/boat_form.html'
    
    def get(self, request, id):
        barco = get_object_or_404(Barco, id=id)
        form = BarcoForm(instance=barco)
        return render(request, self.template_name, {'form': form, 'barco': barco, 'titulo': 'Editar Barco'})
    
    def post(self, request, id):
        barco = get_object_or_404(Barco, id=id)
        form = BarcoForm(request.POST, request.FILES, instance=barco)
        if form.is_valid():
            form.save()
            messages.success(request, 'Barco actualizado exitosamente.')
            return redirect('admin_panel:boats_list')
        return render(request, self.template_name, {'form': form, 'barco': barco, 'titulo': 'Editar Barco'})


class AdminBoatDeleteView(AdminRequiredMixin, View):
    def post(self, request, id):
        barco = get_object_or_404(Barco, id=id)
        barco.delete()
        messages.success(request, 'Barco eliminado exitosamente.')
        return redirect('admin_panel:boats_list')


class AdminClientsListView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_panel/clients_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientes'] = User.objects.filter(is_staff=False).order_by('email')
        return context


class AdminClientDeleteView(AdminRequiredMixin, View):
    def post(self, request, id):
        cliente = get_object_or_404(User, id=id, is_staff=False)
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect('admin_panel:clients_list')


class AdminReservationsListView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_panel/reservations_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservas'] = Reserva.objects.all().order_by('-created_at')
        return context


class AdminReservationDetailView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_panel/reservation_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reserva = get_object_or_404(Reserva, id=kwargs.get('id'))
        context['reserva'] = reserva
        context['lineas'] = LineaReserva.objects.filter(reserva=reserva)
        return context


class AdminChangeReservationStatusView(AdminRequiredMixin, View):
    def post(self, request, id):
        reserva = get_object_or_404(Reserva, id=id)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in dict(Reserva.ESTADO_CHOICES):
            reserva.estado = nuevo_estado
            reserva.save()
            messages.success(request, f'Estado de reserva actualizado a {reserva.get_estado_display()}.')
        else:
            messages.error(request, 'Estado inválido.')
        
        return redirect('admin_panel:reservation_detail', id=id)
