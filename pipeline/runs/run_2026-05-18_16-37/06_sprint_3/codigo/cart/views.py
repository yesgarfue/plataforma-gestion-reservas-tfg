from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from catalog.models import Barco
from .services import get_cart, add_to_cart, update_cart, clear_cart, get_cart_items, get_cart_total

class CartView(View):
    def get(self, request):
        items = get_cart_items(request)
        total = get_cart_total(request)
        return render(request, 'cart/view.html', {
            'items': items,
            'total': total
        })

class AddToCartView(View):
    def post(self, request):
        barco_id = request.POST.get('barco_id')
        cantidad = request.POST.get('cantidad', 1)
        try:
            barco_id = int(barco_id)
            cantidad = int(cantidad)
            if cantidad <= 0:
                messages.error(request, 'La cantidad debe ser mayor a 0.')
                return redirect('catalog:barco_detail', id=barco_id)
            barco = Barco.objects.get(id=barco_id)
            if cantidad > barco.cantidad_disponible:
                messages.error(request, f'Solo hay {barco.cantidad_disponible} unidades disponibles.')
                return redirect('catalog:barco_detail', id=barco_id)
            add_to_cart(request, barco_id, cantidad)
            messages.success(request, f'{barco.nombre} añadido a la cesta.')
        except (ValueError, Barco.DoesNotExist):
            messages.error(request, 'Error al añadir a la cesta.')
        return redirect('catalog:barco_list')

class UpdateCartView(View):
    def post(self, request):
        barco_id = request.POST.get('barco_id')
        cantidad = request.POST.get('cantidad', 0)
        try:
            barco_id = int(barco_id)
            cantidad = int(cantidad)
            update_cart(request, barco_id, cantidad)
            messages.success(request, 'Cesta actualizada.')
        except ValueError:
            messages.error(request, 'Error al actualizar la cesta.')
        return redirect('cart:view')

class ClearCartView(View):
    def post(self, request):
        clear_cart(request)
        messages.success(request, 'Cesta vaciada.')
        return redirect('cart:view')
