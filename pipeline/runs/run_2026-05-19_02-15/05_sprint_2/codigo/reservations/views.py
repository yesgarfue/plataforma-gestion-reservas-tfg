from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from datetime import date
from decimal import Decimal

from cart.services import CartService
from .models import Reserva, LineaReserva
from .forms import ReservationStep1Form, ReservationStep2Form, ReservationStep3Form
from .services.pricing import PricingService
from .services.tracking import TrackingService
from catalog.models import Barco


class ReservationStep1View(View):
    """
    Paso 1: Seleccionar fechas de inicio y fin.
    """
    def get(self, request):
        form = ReservationStep1Form()
        return render(request, 'reservations/step1.html', {'form': form})

    def post(self, request):
        form = ReservationStep1Form(request.POST)
        if form.is_valid():
            request.session['reserva_fecha_inicio'] = str(form.cleaned_data['fecha_inicio'])
            request.session['reserva_fecha_fin'] = str(form.cleaned_data['fecha_fin'])
            request.session.modified = True
            return redirect('reservations:step2')
        return render(request, 'reservations/step1.html', {'form': form})


class ReservationStep2View(View):
    """
    Paso 2: Ingresar datos del cliente y revisar cesta con precios.
    """
    def get(self, request):
        # Verificar que hay fechas en sesión
        if 'reserva_fecha_inicio' not in request.session or 'reserva_fecha_fin' not in request.session:
            messages.error(request, 'Por favor, selecciona las fechas primero.')
            return redirect('reservations:step1')

        # Verificar que hay items en la cesta
        cart_items = CartService.get_cart_items(request)
        if not cart_items:
            messages.error(request, 'Tu cesta está vacía.')
            return redirect('cart:view')

        # Preparar datos iniciales del formulario
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['nombre_cliente'] = request.user.first_name or ''
            initial_data['apellido_cliente'] = request.user.last_name or ''
            initial_data['email_contacto'] = request.user.email
            if hasattr(request.user, 'profile'):
                initial_data['telefono_cliente'] = request.user.profile.telefono or ''

        form = ReservationStep2Form(initial=initial_data)

        # Calcular precios de los items
        fecha_inicio = date.fromisoformat(request.session['reserva_fecha_inicio'])
        fecha_fin = date.fromisoformat(request.session['reserva_fecha_fin'])
        dias = PricingService.calcular_dias(fecha_inicio, fecha_fin)

        items_con_precio = []
        total_reserva = Decimal('0.00')
        for item in cart_items:
            subtotal, _, tasa_combustible = PricingService.calcular_subtotal_linea(
                item['barco'], item['cantidad'], fecha_inicio, fecha_fin
            )
            items_con_precio.append({
                'barco': item['barco'],
                'cantidad': item['cantidad'],
                'precio_dia': item['precio_dia'],
                'tasa_combustible': tasa_combustible,
                'precio_total_dia': item['precio_dia'] + tasa_combustible,
                'subtotal': subtotal,
                'dias': dias,
            })
            total_reserva += Decimal(str(subtotal))

        context = {
            'form': form,
            'items': items_con_precio,
            'total': total_reserva,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'dias': dias,
        }
        return render(request, 'reservations/step2.html', context)

    def post(self, request):
        # Verificar que hay fechas en sesión
        if 'reserva_fecha_inicio' not in request.session or 'reserva_fecha_fin' not in request.session:
            messages.error(request, 'Por favor, selecciona las fechas primero.')
            return redirect('reservations:step1')

        form = ReservationStep2Form(request.POST)
        if form.is_valid():
            request.session['reserva_nombre'] = form.cleaned_data['nombre_cliente']
            request.session['reserva_apellido'] = form.cleaned_data['apellido_cliente']
            request.session['reserva_email'] = form.cleaned_data['email_contacto']
            request.session['reserva_telefono'] = form.cleaned_data['telefono_cliente']
            request.session.modified = True
            return redirect('reservations:step3')

        # Recalcular items para mostrar en caso de error
        cart_items = CartService.get_cart_items(request)
        fecha_inicio = date.fromisoformat(request.session['reserva_fecha_inicio'])
        fecha_fin = date.fromisoformat(request.session['reserva_fecha_fin'])
        dias = PricingService.calcular_dias(fecha_inicio, fecha_fin)

        items_con_precio = []
        total_reserva = Decimal('0.00')
        for item in cart_items:
            subtotal, _, tasa_combustible = PricingService.calcular_subtotal_linea(
                item['barco'], item['cantidad'], fecha_inicio, fecha_fin
            )
            items_con_precio.append({
                'barco': item['barco'],
                'cantidad': item['cantidad'],
                'precio_dia': item['precio_dia'],
                'tasa_combustible': tasa_combustible,
                'precio_total_dia': item['precio_dia'] + tasa_combustible,
                'subtotal': subtotal,
                'dias': dias,
            })
            total_reserva += Decimal(str(subtotal))

        context = {
            'form': form,
            'items': items_con_precio,
            'total': total_reserva,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'dias': dias,
        }
        return render(request, 'reservations/step2.html', context)


class ReservationStep3View(View):
    """
    Paso 3: Seleccionar método de pago y confirmar reserva.
    """
    def get(self, request):
        # Verificar que hay datos en sesión
        required_keys = ['reserva_fecha_inicio', 'reserva_fecha_fin', 'reserva_nombre', 'reserva_email']
        for key in required_keys:
            if key not in request.session:
                messages.error(request, 'Por favor, completa los pasos anteriores.')
                return redirect('reservations:step1')

        # Verificar que hay items en la cesta
        cart_items = CartService.get_cart_items(request)
        if not cart_items:
            messages.error(request, 'Tu cesta está vacía.')
            return redirect('cart:view')

        form = ReservationStep3Form()

        # Calcular total
        fecha_inicio = date.fromisoformat(request.session['reserva_fecha_inicio'])
        fecha_fin = date.fromisoformat(request.session['reserva_fecha_fin'])
        dias = PricingService.calcular_dias(fecha_inicio, fecha_fin)

        items_con_precio = []
        total_reserva = Decimal('0.00')
        for item in cart_items:
            subtotal, _, tasa_combustible = PricingService.calcular_subtotal_linea(
                item['barco'], item['cantidad'], fecha_inicio, fecha_fin
            )
            items_con_precio.append({
                'barco': item['barco'],
                'cantidad': item['cantidad'],
                'precio_dia': item['precio_dia'],
                'tasa_combustible': tasa_combustible,
                'precio_total_dia': item['precio_dia'] + tasa_combustible,
                'subtotal': subtotal,
                'dias': dias,
            })
            total_reserva += Decimal(str(subtotal))

        context = {
            'form': form,
            'items': items_con_precio,
            'total': total_reserva,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'dias': dias,
            'nombre_cliente': request.session.get('reserva_nombre'),
            'apellido_cliente': request.session.get('reserva_apellido'),
            'email_contacto': request.session.get('reserva_email'),
        }
        return render(request, 'reservations/step3.html', context)

    def post(self, request):
        # Verificar que hay datos en sesión
        required_keys = ['reserva_fecha_inicio', 'reserva_fecha_fin', 'reserva_nombre', 'reserva_email']
        for key in required_keys:
            if key not in request.session:
                messages.error(request, 'Por favor, completa los pasos anteriores.')
                return redirect('reservations:step1')

        form = ReservationStep3Form(request.POST)
        if form.is_valid():
            metodo_pago = form.cleaned_data['metodo_pago']

            # Crear la reserva
            fecha_inicio = date.fromisoformat(request.session['reserva_fecha_inicio'])
            fecha_fin = date.fromisoformat(request.session['reserva_fecha_fin'])
            cart_items = CartService.get_cart_items(request)

            # Calcular total
            total_reserva = Decimal('0.00')
            lineas_data = []
            for item in cart_items:
                subtotal, dias, tasa_combustible = PricingService.calcular_subtotal_linea(
                    item['barco'], item['cantidad'], fecha_inicio, fecha_fin
                )
                lineas_data.append({
                    'barco': item['barco'],
                    'cantidad': item['cantidad'],
                    'precio_unitario_dia': item['precio_dia'],
                    'tasa_combustible_dia': tasa_combustible,
                    'subtotal': subtotal,
                })
                total_reserva += Decimal(str(subtotal))

            # Crear reserva
            reserva = Reserva.objects.create(
                cliente=request.user if request.user.is_authenticated else None,
                email_contacto=request.session['reserva_email'],
                nombre_cliente=request.session['reserva_nombre'],
                apellido_cliente=request.session['reserva_apellido'],
                telefono_cliente=request.session.get('reserva_telefono', ''),
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                importe_total=total_reserva,
                metodo_pago=metodo_pago,
                estado='PAGADO' if metodo_pago == 'CONTRA_REEMBOLSO' else 'PENDIENTE_DE_PAGO',
            )

            # Crear líneas de reserva
            for linea_data in lineas_data:
                LineaReserva.objects.create(
                    reserva=reserva,
                    barco=linea_data['barco'],
                    cantidad=linea_data['cantidad'],
                    precio_unitario_dia=linea_data['precio_unitario_dia'],
                    tasa_combustible_dia=linea_data['tasa_combustible_dia'],
                    subtotal=linea_data['subtotal'],
                )

            # Enviar correo de confirmación
            TrackingService.enviar_confirmacion_reserva(reserva)

            # Guardar código de seguimiento en sesión
            request.session['reserva_codigo'] = str(reserva.codigo_seguimiento)
            request.session.modified = True

            # Limpiar cesta
            CartService.clear_cart(request)

            # Limpiar datos de reserva de sesión
            for key in ['reserva_fecha_inicio', 'reserva_fecha_fin', 'reserva_nombre', 'reserva_apellido', 'reserva_email', 'reserva_telefono']:
                if key in request.session:
                    del request.session[key]
            request.session.modified = True

            # Redirigir según método de pago
            if metodo_pago == 'PAYPAL':
                return redirect('payments:paypal_redirect')
            else:
                return redirect('reservations:confirmation')

        # Recalcular items para mostrar en caso de error
        cart_items = CartService.get_cart_items(request)
        fecha_inicio = date.fromisoformat(request.session['reserva_fecha_inicio'])
        fecha_fin = date.fromisoformat(request.session['reserva_fecha_fin'])
        dias = PricingService.calcular_dias(fecha_inicio, fecha_fin)

        items_con_precio = []
        total_reserva = Decimal('0.00')
        for item in cart_items:
            subtotal, _, tasa_combustible = PricingService.calcular_subtotal_linea(
                item['barco'], item['cantidad'], fecha_inicio, fecha_fin
            )
            items_con_precio.append({
                'barco': item['barco'],
                'cantidad': item['cantidad'],
                'precio_dia': item['precio_dia'],
                'tasa_combustible': tasa_combustible,
                'precio_total_dia': item['precio_dia'] + tasa_combustible,
                'subtotal': subtotal,
                'dias': dias,
            })
            total_reserva += Decimal(str(subtotal))

        context = {
            'form': form,
            'items': items_con_precio,
            'total': total_reserva,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'dias': dias,
            'nombre_cliente': request.session.get('reserva_nombre'),
            'apellido_cliente': request.session.get('reserva_apellido'),
            'email_contacto': request.session.get('reserva_email'),
        }
        return render(request, 'reservations/step3.html', context)


class ReservationConfirmationView(View):
    """
    Confirmación de reserva después del pago.
    """
    def get(self, request):
        codigo = request.GET.get('codigo')
        if not codigo and 'reserva_codigo' in request.session:
            codigo = request.session['reserva_codigo']

        if not codigo:
            messages.error(request, 'No se encontró el código de seguimiento.')
            return redirect('home')

        try:
            reserva = Reserva.objects.get(codigo_seguimiento=codigo)
        except Reserva.DoesNotExist:
            messages.error(request, 'Reserva no encontrada.')
            return redirect('home')

        context = {
            'reserva': reserva,
            'lineas': reserva.lineas.all(),
        }
        return render(request, 'reservations/confirmation.html', context)


class TrackingView(View):
    """
    Búsqueda de reserva por código de seguimiento.
    """
    def get(self, request):
        return render(request, 'reservations/tracking.html')

    def post(self, request):
        codigo = request.POST.get('codigo', '').strip()
        if not codigo:
            messages.error(request, 'Por favor, ingresa un código de seguimiento.')
            return render(request, 'reservations/tracking.html')

        try:
            reserva = Reserva.objects.get(codigo_seguimiento=codigo)
            return redirect('reservations:tracking_detail', codigo=codigo)
        except Reserva.DoesNotExist:
            messages.error(request, 'No se encontró una reserva con ese código.')
            return render(request, 'reservations/tracking.html')


class TrackingDetailView(View):
    """
    Detalle de seguimiento de una reserva.
    """
    def get(self, request, codigo):
        try:
            reserva = Reserva.objects.get(codigo_seguimiento=codigo)
        except Reserva.DoesNotExist:
            messages.error(request, 'Reserva no encontrada.')
            return redirect('reservations:tracking')

        context = {
            'reserva': reserva,
            'lineas': reserva.lineas.all(),
        }
        return render(request, 'reservations/tracking_detail.html', context)


@method_decorator(login_required, name='dispatch')
class MyReservationsView(View):
    """
    Listado de reservas del usuario autenticado.
    """
    def get(self, request):
        reservas = Reserva.objects.filter(cliente=request.user).prefetch_related('lineas')
        context = {
            'reservas': reservas,
        }
        return render(request, 'reservations/my_reservations.html', context)


class CancelReservationView(View):
    """
    Cancelar una reserva.
    """
    def post(self, request, codigo):
        try:
            reserva = Reserva.objects.get(codigo_seguimiento=codigo)
        except Reserva.DoesNotExist:
            messages.error(request, 'Reserva no encontrada.')
            return redirect('reservations:tracking')

        # Solo se pueden cancelar reservas en estado PENDIENTE_DE_PAGO
        if reserva.estado != 'PENDIENTE_DE_PAGO':
            messages.error(request, 'Solo se pueden cancelar reservas pendientes de pago.')
            return redirect('reservations:tracking_detail', codigo=codigo)

        reserva.delete()
        messages.success(request, 'Reserva cancelada correctamente.')
        return redirect('reservations:tracking')
