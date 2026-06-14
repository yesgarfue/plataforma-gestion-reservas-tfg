from django.shortcuts import render
from django.views import View
from catalog.models import Barco, Categoria
from cart.services import get_cart_items, get_cart_total

class HomeView(View):
    def get(self, request):
        barcos = Barco.objects.all()[:10]
        categorias = Categoria.objects.all()
        barcos_por_categoria = {}
        for barco in barcos:
            if barco.categoria.nombre not in barcos_por_categoria:
                barcos_por_categoria[barco.categoria.nombre] = []
            barcos_por_categoria[barco.categoria.nombre].append(barco)
        
        cart_items = get_cart_items(request)
        cart_total = get_cart_total(request)
        
        return render(request, 'home.html', {
            'barcos': barcos,
            'barcos_por_categoria': barcos_por_categoria,
            'categorias': categorias,
            'cart_items': cart_items,
            'cart_total': cart_total,
        })
