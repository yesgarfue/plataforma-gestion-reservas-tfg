from decimal import Decimal
from catalog.models import Barco


class CartService:
    CART_SESSION_KEY = 'cart'

    @staticmethod
    def get_cart(request):
        if CartService.CART_SESSION_KEY not in request.session:
            request.session[CartService.CART_SESSION_KEY] = {}
        return request.session[CartService.CART_SESSION_KEY]

    @staticmethod
    def add_to_cart(request, barco_id, cantidad):
        cart = CartService.get_cart(request)
        barco_id_str = str(barco_id)
        
        if barco_id_str in cart:
            cart[barco_id_str]['cantidad'] += cantidad
        else:
            barco = Barco.objects.get(id=barco_id)
            cart[barco_id_str] = {
                'nombre': barco.nombre,
                'precio_dia': str(barco.precio_dia),
                'cantidad': cantidad,
                'disponibilidad': barco.disponibilidad,
            }
        
        request.session[CartService.CART_SESSION_KEY] = cart
        request.session.modified = True

    @staticmethod
    def update_cart(request, barco_id, cantidad):
        cart = CartService.get_cart(request)
        barco_id_str = str(barco_id)
        
        if barco_id_str in cart:
            if cantidad <= 0:
                del cart[barco_id_str]
            else:
                cart[barco_id_str]['cantidad'] = cantidad
        
        request.session[CartService.CART_SESSION_KEY] = cart
        request.session.modified = True

    @staticmethod
    def clear_cart(request):
        request.session[CartService.CART_SESSION_KEY] = {}
        request.session.modified = True

    @staticmethod
    def get_cart_items(request):
        cart = CartService.get_cart(request)
        items = []
        for barco_id, item in cart.items():
            try:
                barco = Barco.objects.get(id=int(barco_id))
                items.append({
                    'barco': barco,
                    'cantidad': item['cantidad'],
                    'precio_dia': Decimal(item['precio_dia']),
                    'subtotal': Decimal(item['precio_dia']) * item['cantidad'],
                })
            except Barco.DoesNotExist:
                pass
        return items

    @staticmethod
    def get_cart_total(request):
        items = CartService.get_cart_items(request)
        total = sum(item['subtotal'] for item in items)
        return total
