from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from .services import CartService
from catalog.models import Barco
from django.contrib import messages


class CartView(View):
    def get(self, request):
        # Si el usuario es administrador, vaciar cesta
        if request.user.is_authenticated and request.user.is_staff:
            CartService.clear_cart(request)
            messages.info(request, 'La cesta ha sido vaciada para administradores.')
            return redirect('home')

        items = CartService.get_cart_items(request)
        total = CartService.get_cart_total(request)
        return render(request, 'cart/view.html', {
            'items': items,
            'total': total,
        })


class AddToCartView(View):
    def post(self, request):
        # Si el usuario es administrador, no permitir agregar a cesta
        if request.user.is_authenticated and request.user.is_staff:
            messages.error(request, 'Los administradores no pueden agregar barcos a la cesta.')
            return redirect('catalog:barco_list')

        barco_id = request.POST.get('barco_id')
        cantidad = request.POST.get('cantidad', 1)
        
        try:
            barco_id = int(barco_id)
            cantidad = int(cantidad)
            
            if cantidad <= 0:
                messages.error(request, 'La cantidad debe ser mayor a 0.')
                return redirect('catalog:barco_detail', id=barco_id)
            
            barco = Barco.objects.get(id=barco_id, activo=True)
            
            if cantidad > barco.disponibilidad:
                messages.error(request, f'Solo hay {barco.disponibilidad} unidades disponibles.')
                return redirect('catalog:barco_detail', id=barco_id)
            
            CartService.add_to_cart(request, barco_id, cantidad)
            messages.success(request, f'{barco.nombre} añadido a la cesta.')
            return redirect('cart:view')
        except (ValueError, Barco.DoesNotExist):
            messages.error(request, 'Error al añadir el barco a la cesta.')
            return redirect('catalog:barco_list')


class UpdateCartView(View):
    def post(self, request):
        barco_id = request.POST.get('barco_id')
        cantidad = request.POST.get('cantidad', 0)
        
        try:
            barco_id = int(barco_id)
            cantidad = int(cantidad)
            CartService.update_cart(request, barco_id, cantidad)
            messages.success(request, 'Cesta actualizada.')
        except (ValueError, TypeError):
            messages.error(request, 'Error al actualizar la cesta.')
        
        return redirect('cart:view')


class ClearCartView(View):
    def post(self, request):
        CartService.clear_cart(request)
        messages.success(request, 'Cesta vaciada.')
        return redirect('cart:view')
