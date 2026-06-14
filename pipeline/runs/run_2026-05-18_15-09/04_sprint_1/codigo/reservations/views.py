from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.http import JsonResponse
from catalog.models import Barco
from .models import LineaCarrito, Reserva, LineaReserva
from .forms import AgregarCarritoForm, DatosClienteForm, MetodoPagoForm
from datetime import date
import uuid


def get_session_id(request):
    if 'carrito_sesion_id' not in request.session:
        request.session['carrito_sesion_id'] = str(uuid.uuid4())
    return request.session['carrito_sesion_id']


class CartView(TemplateView):
    template_name = 'reservations/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sesion_id = get_session_id(self.request)
        lineas = LineaCarrito.objects.filter(sesion_id=sesion_id)
        total = sum(linea.barco.precio_dia * linea.cantidad * (linea.fecha_fin - linea.fecha_inicio).days for linea in lineas)
        context['lineas'] = lineas
        context['total'] = total
        return context


class AddToCartView(View):
    def post(self, request):
        barco_id = request.POST.get('barco_id')
        barco = get_object_or_404(Barco, id=barco_id)
        form = AgregarCarritoForm(request.POST)
        
        if form.is_valid():
            sesion_id = get_session_id(request)
            cantidad = form.cleaned_data['cantidad']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            
            LineaCarrito.objects.create(
                sesion_id=sesion_id,
                barco=barco,
                cantidad=cantidad,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            messages.success(request, f'{barco.nombre} añadido a la cesta.')
            return redirect('reservations:cart')
        else:
            messages.error(request, 'Error al añadir a la cesta. Verifica los datos.')
            return redirect('catalog:barco_detail', id=barco_id)


class UpdateCartView(View):
    def post(self, request):
        linea_id = request.POST.get('linea_id')
        cantidad = request.POST.get('cantidad')
        linea = get_object_or_404(LineaCarrito, id=linea_id)
        
        try:
            cantidad = int(cantidad)
            if cantidad > 0:
                linea.cantidad = cantidad
                linea.save()
                messages.success(request, 'Cantidad actualizada.')
            else:
                linea.delete()
                messages.success(request, 'Artículo eliminado de la cesta.')
        except ValueError:
            messages.error(request, 'Cantidad inválida.')
        
        return redirect('reservations:cart')


class ClearCartView(View):
    def post(self, request):
        sesion_id = get_session_id(request)
        LineaCarrito.objects.filter(sesion_id=sesion_id).delete()
        messages.success(request, 'Cesta vaciada.')
        return redirect('reservations:cart')


class ReservationStep1View(View):
    template_name = 'reservations/step1.html'

    def get(self, request):
        sesion_id = get_session_id(request)
        lineas = LineaCarrito.objects.filter(sesion_id=sesion_id)
        if not lineas.exists():
            messages.error(request, 'Tu cesta está vacía.')
            return redirect('reservations:cart')
        total = sum(linea.barco.precio_dia * linea.cantidad * (linea.fecha_fin - linea.fecha_inicio).days for linea in lineas)
        return render(request, self.template_name, {'lineas': lineas, 'total': total})

    def post(self, request):
        sesion_id = get_session_id(request)
        lineas = LineaCarrito.objects.filter(sesion_id=sesion_id)
        if not lineas.exists():
            messages.error(request, 'Tu cesta está vacía.')
            return redirect('reservations:cart')
        request.session['reserva_paso1_confirmado'] = True
        return redirect('reservations:step2')


class ReservationStep2View(View):
    template_name = 'reservations/step2.html'

    def get(self, request):
        if not request.session.get('reserva_paso1_confirmado'):
            messages.error(request, 'Debes completar el paso 1 primero.')
            return redirect('reservations:step1')
        form = DatosClienteForm()
        if request.user.is_authenticated:
            form.initial = {'nombre_cliente': request.user.get_full_name() or request.user.username, 'email_contacto': request.user.email}
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.session.get('reserva_paso1_confirmado'):
            messages.error(request, 'Debes completar el paso 1 primero.')
            return redirect('reservations:step1')
        form = DatosClienteForm(request.POST)
        if form.is_valid():
            request.session['datos_cliente'] = form.cleaned_data
            return redirect('reservations:step3')
        return render(request, self.template_name, {'form': form})


class ReservationStep3View(View):
    template_name = 'reservations/step3.html'

    def get(self, request):
        if not request.session.get('datos_cliente'):
            messages.error(request, 'Debes completar el paso 2 primero.')
            return redirect('reservations:step2')
        form = MetodoPagoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.session.get('datos_cliente'):
            messages.error(request, 'Debes completar el paso 2 primero.')
            return redirect('reservations:step2')
        form = MetodoPagoForm(request.POST)
        if form.is_valid():
            sesion_id = get_session_id(request)
            lineas = LineaCarrito.objects.filter(sesion_id=sesion_id)
            datos_cliente = request.session.get('datos_cliente')
            
            total = sum(linea.barco.precio_dia * linea.cantidad * (linea.fecha_fin - linea.fecha_inicio).days for linea in lineas)
            
            reserva = Reserva.objects.create(
                codigo_seguimiento=str(uuid.uuid4())[:32],
                cliente=request.user if request.user.is_authenticated else None,
                nombre_cliente=datos_cliente['nombre_cliente'],
                email_contacto=datos_cliente['email_contacto'],
                telefono=datos_cliente.get('telefono', ''),
                metodo_pago=form.cleaned_data['metodo_pago'],
                importe_total=total,
                fecha_inicio=min(linea.fecha_inicio for linea in lineas),
                fecha_fin=max(linea.fecha_fin for linea in lineas),
            )
            
            for linea in lineas:
                LineaReserva.objects.create(
                    reserva=reserva,
                    barco=linea.barco,
                    cantidad=linea.cantidad,
                    precio_unitario_dia=linea.barco.precio_dia,
                    tasa_combustible_dia=0
                )
            
            LineaCarrito.objects.filter(sesion_id=sesion_id).delete()
            request.session.pop('reserva_paso1_confirmado', None)
            request.session.pop('datos_cliente', None)
            request.session.pop('carrito_sesion_id', None)
            
            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('reservations:confirmation')
        return render(request, self.template_name, {'form': form})


class ConfirmationView(TemplateView):
    template_name = 'reservations/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservas = Reserva.objects.all().order_by('-created_at')[:1]
        if reservas:
            context['reserva'] = reservas[0]
        return context


class CancelReservationView(View):
    def post(self, request, codigo):
        reserva = get_object_or_404(Reserva, codigo_seguimiento=codigo)
        if reserva.estado == 'PENDIENTE_DE_PAGO':
            reserva.delete()
            messages.success(request, 'Reserva cancelada.')
        else:
            messages.error(request, 'No se puede cancelar una reserva que ya ha sido pagada.')
        return redirect('home')
