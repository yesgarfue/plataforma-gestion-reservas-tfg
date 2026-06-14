from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
import uuid
from decimal import Decimal

from catalog.models import Barco
from cart.services import get_cart_items, get_cart_total, clear_cart
from accounts.models import User
from .models import Reserva, LineaReserva
from .forms import ReservationStep1Form, ReservationStep2Form, ReservationStep3Form
from .services.email import EmailService
from .services.paypal import PayPalService

class ReservationStep1View(View):
    """Paso 1: Datos del cliente y fechas"""
    
    def get(self, request):
        cart_items = get_cart_items(request)
        if not cart_items:
            messages.error(request, 'Tu cesta está vacía.')
            return redirect('cart:view')
        
        form = ReservationStep1Form()
        
        # Si el usuario está autenticado, prellenar datos
        if 'user_id' in request.session:
            try:
                user = User.objects.get(id=request.session['user_id'])
                form.initial = {
                    'nombre_cliente': user.nombre,
                    'email_cliente': user.email,
                    'telefono_cliente': user.telefono,
                }
            except User.DoesNotExist:
                pass
        
        return render(request, 'reservations/step1.html', {
            'form': form,
            'cart_items': cart_items,
            'cart_total': get_cart_total(request),
        })
    
    def post(self, request):
        cart_items = get_cart_items(request)
        if not cart_items:
            messages.error(request, 'Tu cesta está vacía.')
            return redirect('cart:view')
        
        form = ReservationStep1Form(request.POST)
        if form.is_valid():
            # Guardar datos en sesión
            request.session['reservation_step1'] = {
                'fecha_inicio': form.cleaned_data['fecha_inicio'].isoformat(),
                'fecha_fin': form.cleaned_data['fecha_fin'].isoformat(),
                'nombre_cliente': form.cleaned_data['nombre_cliente'],
                'email_cliente': form.cleaned_data['email_cliente'],
                'telefono_cliente': form.cleaned_data['telefono_cliente'],
            }
            request.session.modified = True
            return redirect('reservations:step2')
        
        return render(request, 'reservations/step1.html', {
            'form': form,
            'cart_items': cart_items,
            'cart_total': get_cart_total(request),
        })

class ReservationStep2View(View):
    """Paso 2: Selección del método de pago"""
    
    def get(self, request):
        if 'reservation_step1' not in request.session:
            messages.error(request, 'Por favor, completa el paso 1 primero.')
            return redirect('reservations:step1')
        
        form = ReservationStep2Form()
        cart_items = get_cart_items(request)
        
        # Calcular importe total con tasa de combustible
        cart_total = get_cart_total(request)
        fecha_inicio = datetime.fromisoformat(request.session['reservation_step1']['fecha_inicio']).date()
        fecha_fin = datetime.fromisoformat(request.session['reservation_step1']['fecha_fin']).date()
        dias = (fecha_fin - fecha_inicio).days
        
        tasa_combustible = Decimal('0')
        for item in cart_items:
            if item['barco'].categoria.nombre.lower() != 'velero':
                tasa_combustible += Decimal('50') * dias
        
        importe_total = cart_total + tasa_combustible
        
        return render(request, 'reservations/step2.html', {
            'form': form,
            'cart_items': cart_items,
            'cart_total': cart_total,
            'tasa_combustible': tasa_combustible,
            'importe_total': importe_total,
            'dias': dias,
        })
    
    def post(self, request):
        if 'reservation_step1' not in request.session:
            messages.error(request, 'Por favor, completa el paso 1 primero.')
            return redirect('reservations:step1')
        
        form = ReservationStep2Form(request.POST)
        if form.is_valid():
            request.session['reservation_step2'] = {
                'metodo_pago': form.cleaned_data['metodo_pago'],
            }
            request.session.modified = True
            return redirect('reservations:step3')
        
        cart_items = get_cart_items(request)
        cart_total = get_cart_total(request)
        fecha_inicio = datetime.fromisoformat(request.session['reservation_step1']['fecha_inicio']).date()
        fecha_fin = datetime.fromisoformat(request.session['reservation_step1']['fecha_fin']).date()
        dias = (fecha_fin - fecha_inicio).days
        
        tasa_combustible = Decimal('0')
        for item in cart_items:
            if item['barco'].categoria.nombre.lower() != 'velero':
                tasa_combustible += Decimal('50') * dias
        
        importe_total = cart_total + tasa_combustible
        
        return render(request, 'reservations/step2.html', {
            'form': form,
            'cart_items': cart_items,
            'cart_total': cart_total,
            'tasa_combustible': tasa_combustible,
            'importe_total': importe_total,
            'dias': dias,
        })

class ReservationStep3View(View):
    """Paso 3: Confirmación y pago"""
    
    def get(self, request):
        if 'reservation_step1' not in request.session or 'reservation_step2' not in request.session:
            messages.error(request, 'Por favor, completa los pasos anteriores primero.')
            return redirect('reservations:step1')
        
        form = ReservationStep3Form()
        cart_items = get_cart_items(request)
        
        # Calcular importe total
        cart_total = get_cart_total(request)
        fecha_inicio = datetime.fromisoformat(request.session['reservation_step1']['fecha_inicio']).date()
        fecha_fin = datetime.fromisoformat(request.session['reservation_step1']['fecha_fin']).date()
        dias = (fecha_fin - fecha_inicio).days
        
        tasa_combustible = Decimal('0')
        for item in cart_items:
            if item['barco'].categoria.nombre.lower() != 'velero':
                tasa_combustible += Decimal('50') * dias
        
        importe_total = cart_total + tasa_combustible
        metodo_pago = request.session['reservation_step2']['metodo_pago']
        
        return render(request, 'reservations/step3.html', {
            'form': form,
            'cart_items': cart_items,
            'cart_total': cart_total,
            'tasa_combustible': tasa_combustible,
            'importe_total': importe_total,
            'dias': dias,
            'metodo_pago': metodo_pago,
            'nombre_cliente': request.session['reservation_step1']['nombre_cliente'],
            'email_cliente': request.session['reservation_step1']['email_cliente'],
        })
    
    def post(self, request):
        if 'reservation_step1' not in request.session or 'reservation_step2' not in request.session:
            messages.error(request, 'Por favor, completa los pasos anteriores primero.')
            return redirect('reservations:step1')
        
        form = ReservationStep3Form(request.POST)
        if form.is_valid():
            # Crear la reserva
            cart_items = get_cart_items(request)
            cart_total = get_cart_total(request)
            
            fecha_inicio = datetime.fromisoformat(request.session['reservation_step1']['fecha_inicio']).date()
            fecha_fin = datetime.fromisoformat(request.session['reservation_step1']['fecha_fin']).date()
            dias = (fecha_fin - fecha_inicio).days
            
            tasa_combustible = Decimal('0')
            for item in cart_items:
                if item['barco'].categoria.nombre.lower() != 'velero':
                    tasa_combustible += Decimal('50') * dias
            
            importe_total = cart_total + tasa_combustible
            metodo_pago = request.session['reservation_step2']['metodo_pago']
            
            # Generar código de seguimiento único
            codigo_seguimiento = str(uuid.uuid4())[:8].upper()
            
            # Obtener usuario si está autenticado
            cliente = None
            if 'user_id' in request.session:
                try:
                    cliente = User.objects.get(id=request.session['user_id'])
                except User.DoesNotExist:
                    pass
            
            # Crear reserva
            reserva = Reserva.objects.create(
                codigo_seguimiento=codigo_seguimiento,
                estado='PENDIENTE_DE_PAGO',
                cliente=cliente,
                nombre_cliente=request.session['reservation_step1']['nombre_cliente'],
                email_cliente=request.session['reservation_step1']['email_cliente'],
                telefono_cliente=request.session['reservation_step1']['telefono_cliente'],
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                metodo_pago=metodo_pago,
                importe_total=importe_total,
                tasa_combustible=tasa_combustible,
            )
            
            # Crear líneas de reserva
            for item in cart_items:
                LineaReserva.objects.create(
                    reserva=reserva,
                    barco=item['barco'],
                    cantidad=item['cantidad'],
                    precio_unitario_dia=item['barco'].precio_dia,
                )
            
            # Enviar correo de confirmación
            EmailService.send_reservation_confirmation(reserva)
            
            # Limpiar sesión de reserva
            if 'reservation_step1' in request.session:
                del request.session['reservation_step1']
            if 'reservation_step2' in request.session:
                del request.session['reservation_step2']
            
            # Procesar pago según método seleccionado
            if metodo_pago == 'PAYPAL':
                # Redirigir a PayPal
                request.session['reserva_id'] = reserva.id
                request.session.modified = True
                return redirect('reservations:paypal_return')  # Placeholder para integración real
            else:
                # Contra-reembolso: marcar como pendiente de pago
                clear_cart(request)
                request.session['reserva_id'] = reserva.id
                request.session.modified = True
                messages.success(request, f'Reserva creada exitosamente. Código de seguimiento: {codigo_seguimiento}')
                return redirect('reservations:confirmation')
        
        cart_items = get_cart_items(request)
        cart_total = get_cart_total(request)
        fecha_inicio = datetime.fromisoformat(request.session['reservation_step1']['fecha_inicio']).date()
        fecha_fin = datetime.fromisoformat(request.session['reservation_step1']['fecha_fin']).date()
        dias = (fecha_fin - fecha_inicio).days
        
        tasa_combustible = Decimal('0')
        for item in cart_items:
            if item['barco'].categoria.nombre.lower() != 'velero':
                tasa_combustible += Decimal('50') * dias
        
        importe_total = cart_total + tasa_combustible
        metodo_pago = request.session['reservation_step2']['metodo_pago']
        
        return render(request, 'reservations/step3.html', {
            'form': form,
            'cart_items': cart_items,
            'cart_total': cart_total,
            'tasa_combustible': tasa_combustible,
            'importe_total': importe_total,
            'dias': dias,
            'metodo_pago': metodo_pago,
            'nombre_cliente': request.session['reservation_step1']['nombre_cliente'],
            'email_cliente': request.session['reservation_step1']['email_cliente'],
        })

class ReservationConfirmationView(View):
    """Vista de confirmación de reserva"""
    
    def get(self, request):
        reserva_id = request.session.get('reserva_id')
        if not reserva_id:
            messages.error(request, 'No hay reserva para mostrar.')
            return redirect('core:home')
        
        try:
            reserva = Reserva.objects.get(id=reserva_id)
            clear_cart(request)
            if 'reserva_id' in request.session:
                del request.session['reserva_id']
            request.session.modified = True
            return render(request, 'reservations/confirmation.html', {'reserva': reserva})
        except Reserva.DoesNotExist:
            messages.error(request, 'Reserva no encontrada.')
            return redirect('core:home')

class TrackReservationView(View):
    """Vista para seguimiento de reserva por código"""
    
    def get(self, request):
        return render(request, 'reservations/track.html')
    
    def post(self, request):
        codigo = request.POST.get('codigo_seguimiento', '').strip()
        if not codigo:
            messages.error(request, 'Por favor, ingresa un código de seguimiento.')
            return render(request, 'reservations/track.html')
        
        try:
            reserva = Reserva.objects.get(codigo_seguimiento=codigo)
            return render(request, 'reservations/track.html', {'reserva': reserva})
        except Reserva.DoesNotExist:
            messages.error(request, 'No se encontró una reserva con ese código.')
            return render(request, 'reservations/track.html')

class MyReservationsView(View):
    """Vista de mis reservas (requiere login)"""
    
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('accounts:login')
        
        try:
            user = User.objects.get(id=user_id)
            reservas = Reserva.objects.filter(cliente=user).order_by('-created_at')
            return render(request, 'reservations/my_reservations.html', {'reservas': reservas})
        except User.DoesNotExist:
            return redirect('accounts:login')

class CancelReservationView(View):
    """Vista para cancelar una reserva"""
    
    def post(self, request, id):
        try:
            reserva = Reserva.objects.get(id=id)
            if reserva.estado == 'PENDIENTE_DE_PAGO':
                reserva.delete()
                messages.success(request, 'Reserva cancelada exitosamente.')
            else:
                messages.error(request, 'No se puede cancelar una reserva que ya ha sido pagada.')
        except Reserva.DoesNotExist:
            messages.error(request, 'Reserva no encontrada.')
        
        return redirect('reservations:track')

class PayPalReturnView(View):
    """Vista de retorno de PayPal"""
    
    def get(self, request):
        # Placeholder para integración real con PayPal
        reserva_id = request.session.get('reserva_id')
        if reserva_id:
            try:
                reserva = Reserva.objects.get(id=reserva_id)
                reserva.estado = 'PAGADO'
                reserva.save()
                messages.success(request, 'Pago realizado exitosamente.')
            except Reserva.DoesNotExist:
                pass
        
        return redirect('reservations:confirmation')

class PayPalCancelView(View):
    """Vista de cancelación de PayPal"""
    
    def get(self, request):
        messages.error(request, 'El pago fue cancelado.')
        return redirect('reservations:step3')
