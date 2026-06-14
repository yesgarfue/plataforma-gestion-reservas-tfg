def get_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']

def add_to_cart(request, barco_id, cantidad):
    cart = get_cart(request)
    barco_id_str = str(barco_id)
    if barco_id_str in cart:
        cart[barco_id_str]['cantidad'] += cantidad
    else:
        cart[barco_id_str] = {'cantidad': cantidad}
    request.session.modified = True

def update_cart(request, barco_id, cantidad):
    cart = get_cart(request)
    barco_id_str = str(barco_id)
    if cantidad <= 0:
        if barco_id_str in cart:
            del cart[barco_id_str]
    else:
        if barco_id_str in cart:
            cart[barco_id_str]['cantidad'] = cantidad
    request.session.modified = True

def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True

def get_cart_items(request):
    from catalog.models import Barco
    cart = get_cart(request)
    items = []
    for barco_id_str, item in cart.items():
        try:
            barco = Barco.objects.get(id=int(barco_id_str))
            items.append({
                'barco': barco,
                'cantidad': item['cantidad'],
                'subtotal': barco.precio_dia * item['cantidad']
            })
        except Barco.DoesNotExist:
            pass
    return items

def get_cart_total(request):
    items = get_cart_items(request)
    return sum(item['subtotal'] for item in items)
