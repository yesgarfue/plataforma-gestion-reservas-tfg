from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from reservations.models import Reserva
from .forms import PayPalPaymentForm, CashOnDeliveryForm
from .services.paypal import PayPalService
from .services.cash_on_delivery import CashOnDeliveryService
from .models import PagoPayPal, PagoContraReembolso


class PayPalRedirectView(View):
    """
    Redirige al usuario a PayPal para completar el pago.
    """
    def get(self, request):
        # Obtener la reserva más reciente del usuario
        if request.user.is_authenticated:
            reserva = Reserva.objects.filter(cliente=request.user).order_by('-fecha_creacion').first()
        else:
            # Si no está autenticado, buscar por sesión
            codigo = request.session.get('reserva_codigo')
            if codigo:
                try:
                    reserva = Reserva.objects.get(codigo_seguimiento=codigo)
                except Reserva.DoesNotExist:
                    messages.error(request, 'Reserva no encontrada.')
                    return redirect('home')
            else:
                messages.error(request, 'No hay reserva para procesar.')
                return redirect('home')

        if not reserva:
            messages.error(request, 'No hay reserva para procesar.')
            return redirect('home')

        # Crear registro de pago PayPal
        pago_paypal, created = PagoPayPal.objects.get_or_create(
            reserva=reserva,
            defaults={'estado': 'PENDIENTE'}
        )

        # Generar URLs de retorno
        return_url = request.build_absolute_uri('/pago/paypal/return/')
        cancel_url = request.build_absolute_uri('/pago/paypal/cancel/')

        # Crear pago en PayPal
        paypal_url = PayPalService.crear_pago(reserva, return_url, cancel_url)
        if paypal_url:
            return redirect(paypal_url)
        else:
            messages.error(request, 'Error al procesar el pago con PayPal.')
            return redirect('reservations:confirmation', codigo=reserva.codigo_seguimiento)

    def post(self, request):
        return self.get(request)


class PayPalReturnView(View):
    """
    Maneja el retorno de PayPal después de un pago exitoso.
    """
    def get(self, request):
        token = request.GET.get('token')
        payerid = request.GET.get('PayerID')

        if not token or not payerid:
            messages.error(request, 'Error en la respuesta de PayPal.')
            return redirect('home')

        # Ejecutar el pago
        if PayPalService.ejecutar_pago(token):
            # Buscar la reserva asociada
            try:
                pago_paypal = PagoPayPal.objects.get(transaction_id=token)
                reserva = pago_paypal.reserva
                reserva.estado = 'PAGADO'
                reserva.save()
                pago_paypal.estado = 'COMPLETADO'
                pago_paypal.save()
                messages.success(request, 'Pago completado exitosamente.')
                return redirect('reservations:confirmation', codigo=reserva.codigo_seguimiento)
            except PagoPayPal.DoesNotExist:
                messages.error(request, 'No se encontró el registro de pago.')
                return redirect('home')
        else:
            messages.error(request, 'Error al completar el pago.')
            return redirect('home')


class PayPalCancelView(View):
    """
    Maneja la cancelación de un pago en PayPal.
    """
    def get(self, request):
        messages.warning(request, 'Has cancelado el pago con PayPal.')
        return redirect('reservations:step3')


class CashOnDeliveryView(View):
    """
    Procesa pagos contra reembolso.
    """
    def get(self, request):
        # Obtener la reserva más reciente
        if request.user.is_authenticated:
            reserva = Reserva.objects.filter(cliente=request.user).order_by('-fecha_creacion').first()
        else:
            codigo = request.session.get('reserva_codigo')
            if codigo:
                try:
                    reserva = Reserva.objects.get(codigo_seguimiento=codigo)
                except Reserva.DoesNotExist:
                    messages.error(request, 'Reserva no encontrada.')
                    return redirect('home')
            else:
                messages.error(request, 'No hay reserva para procesar.')
                return redirect('home')

        if not reserva:
            messages.error(request, 'No hay reserva para procesar.')
            return redirect('home')

        form = CashOnDeliveryForm()
        context = {
            'form': form,
            'reserva': reserva,
        }
        return render(request, 'payments/cash_on_delivery.html', context)

    def post(self, request):
        # Obtener la reserva más reciente
        if request.user.is_authenticated:
            reserva = Reserva.objects.filter(cliente=request.user).order_by('-fecha_creacion').first()
        else:
            codigo = request.session.get('reserva_codigo')
            if codigo:
                try:
                    reserva = Reserva.objects.get(codigo_seguimiento=codigo)
                except Reserva.DoesNotExist:
                    messages.error(request, 'Reserva no encontrada.')
                    return redirect('home')
            else:
                messages.error(request, 'No hay reserva para procesar.')
                return redirect('home')

        if not reserva:
            messages.error(request, 'No hay reserva para procesar.')
            return redirect('home')

        form = CashOnDeliveryForm(request.POST)
        if form.is_valid():
            # Procesar pago contra reembolso
            if CashOnDeliveryService.procesar_pago(reserva):
                # Crear registro de pago
                PagoContraReembolso.objects.get_or_create(
                    reserva=reserva,
                    defaults={'estado': 'PAGADO'}
                )
                messages.success(request, 'Pago contra reembolso confirmado.')
                return redirect('reservations:confirmation', codigo=reserva.codigo_seguimiento)
            else:
                messages.error(request, 'Error al procesar el pago.')
        
        context = {
            'form': form,
            'reserva': reserva,
        }
        return render(request, 'payments/cash_on_delivery.html', context)
