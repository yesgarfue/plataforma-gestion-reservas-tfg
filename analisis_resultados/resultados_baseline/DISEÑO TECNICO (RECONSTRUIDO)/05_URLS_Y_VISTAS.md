# 05 — URLs y Vistas

[← Volver al índice](00_INDICE.md)

---

## URL raíz — `ecommerce/urls.py`

| URL | Vista | Descripción |
|---|---|---|
| `/securelogin/` | `admin.site.urls` | Panel de administración Django (URL ofuscada) |
| `/` | `ecommerce.views.home` | Página principal |
| `/store/` | include `store.urls` | Catálogo de barcos |
| `/cart/` | include `carts.urls` | Carrito de reservas |
| `/accounts/` | include `accounts.urls` | Autenticación y perfiles |
| `/orders/` | include `orders.urls` | Checkout y gestión de reservas |

Los archivos media se sirven en desarrollo vía `static(settings.MEDIA_URL, ...)`.

---

## App `store` — `store/urls.py`

| URL pattern | Vista | Login req. | Admin req. | Descripción |
|---|---|---|---|---|
| `/store/` | `store` | No | No | Listado de barcos con filtros |
| `/store/category/<slug>/` | `store` | No | No | Barcos filtrados por categoría |
| `/store/category/<slug>/<slug>/` | `product_detail` | No | No | Detalle de un barco |
| `/store/search/` | `search` | No | No | Búsqueda por keyword o código de seguimiento |
| `/store/submit_review/<int>/` | `submit_review` | No | No | Enviar/actualizar reseña (POST) |
| `/store/ships` | `product_list` | ✅ | ✅ admin | Lista de barcos para admin |
| `/store/edit_ship/<int>/` | `edit_ship` | ✅ | ✅ admin | Editar barco |
| `/store/delete_ship/<int>/` | `delete_ship` | ✅ | ✅ admin | Eliminar barco |
| `/store/create_ship/` | `create_ship` | ✅ | ✅ admin | Crear barco |

### Detalles de vistas `store`

**`store(request, category_slug=None)`** — `store/views.py:20`
- Filtros: categoría, puerto, fabricante, rango de precio, capacidad, fechas de disponibilidad.
- Paginación: 6 barcos por página.
- Calcula `unavailable_products` según reservas solapadas.

**`product_detail(request, category_slug, product_slug)`** — `store/views.py:107`
- Obtiene el barco y genera eventos de calendario (FullCalendar) con fechas reservadas.
- `in_cart` indica si el barco está ya en el carrito del usuario.

**`search(request)`** — `store/views.py:133`
- Búsqueda por `keyword` en nombre y descripción del barco.
- Búsqueda por `reservation` (código de seguimiento) que muestra el estado de la reserva.
- Si la reserva está en estado "Pendiente de pago" renderiza `orders/order_incomplete.html`; si no, `orders/order_complete.html`.

**`submit_review(request, product_id)`** — `store/views.py:205`
- Si el usuario ya tiene reseña del producto la actualiza; si no, crea una nueva.
- No tiene `@login_required` — si se envía sin autenticar, `request.user.id` falla silenciosamente.

---

## App `carts` — `carts/urls.py`

| URL pattern | Vista | Login req. | Descripción |
|---|---|---|---|
| `/cart/` | `cart` | No | Ver carrito (bloqueado para admins) |
| `/cart/add_cart/<int>/` | `add_cart` | No | Añadir barco al carrito |
| `/cart/remove_cart/<int>/<int>/` | `remove_cart` | No | Decrementar cantidad |
| `/cart/remove_cart_item/<int>/<int>/` | `remove_cart_item` | No | Eliminar ítem completo |
| `/cart/checkout/` | `checkout` | No | Ver resumen de checkout con validación de disponibilidad |
| `/cart/update_cart/` | `update_cart` | No | Actualizar fechas de reserva en carrito (POST) |

### Detalles de vistas `carts`

**`cart`** y **`checkout`** tienen el decorador `@user_passes_test(lambda u: u.id is None or not u.is_admin)` — los administradores son redirigidos automáticamente y no pueden hacer reservas.

**`checkout`** verifica disponibilidad de cada ítem antes de mostrar el resumen; si hay conflicto, redirige al carrito con mensaje de error.

**`_cart_id(request)`** — función auxiliar que devuelve `request.session.session_key` (o crea sesión si no existe). **⚠️ Está duplicada:** definida en `carts/views.py:12` Y en `orders/views.py:36`.

---

## App `accounts` — `accounts/urls.py`

| URL pattern | Vista | Login req. | Admin req. | Descripción |
|---|---|---|---|---|
| `/accounts/register/` | `register` | No | No | Registro de usuario |
| `/accounts/login/` | `login` | No | No | Login |
| `/accounts/logout/` | `logout` | ✅ | No | Logout |
| `/accounts/` | `dashboard` | ✅ | No | Dashboard (mismo que `/accounts/dashboard/`) |
| `/accounts/dashboard/` | `dashboard` | ✅ | No | Dashboard de usuario |
| `/accounts/forgotPassword/` | `forgotPassword` | No | No | Formulario recuperar contraseña |
| `/accounts/resetpassword_validate/<b64>/<token>/` | `resetpassword_validate` | No | No | Valida token de reset |
| `/accounts/resetPassword/` | `resetPassword` | No | No | Formulario nueva contraseña |
| `/accounts/activate/<b64>/<token>/` | `activate` | No | No | Activación de cuenta por email |
| `/accounts/my_orders/` | `my_orders` | No* | No | Mis reservas (redirige si no autenticado) |
| `/accounts/edit_profile/` | `edit_profile` | ✅ | No | Editar perfil |
| `/accounts/change_password/` | `change_password` | ✅ | No | Cambiar contraseña |
| `/accounts/users/` | `list_users` | ✅ | ✅ admin | Lista de usuarios (admin) |
| `/accounts/new_user/` | `create_users` | ✅ | ✅ admin | Crear usuario (admin) |
| `/accounts/edit_user/<int>/` | `edit_user` | ✅ | ✅ admin | Editar usuario (admin) |
| `/accounts/delete_user/<int>/` | `delete_user` | ❌ **Sin protección** | No | Eliminar usuario — **vulnerabilidad crítica** |

*`my_orders` usa `if request.user.is_authenticated` en lugar de `@login_required`, que funciona pero es inconsistente.

---

## App `orders` — `orders/urls.py`

| URL pattern | Vista | Login req. | Admin req. | Descripción |
|---|---|---|---|---|
| `/orders/place_order/` | `place_order` | No | No | Crear pedido desde carrito (POST → payments.html) |
| `/orders/payments/<int>/` | `payments` | No | No | Confirmar pago PayPal (POST JSON) |
| `/orders/order_complete/` | `order_complete` | No | No | Página de confirmación post-pago |
| `/orders/mark_pending/<int>/` | `mark_pending` | No | No | Confirmar reserva contra-reembolso |
| `/orders/reservas/` | `order_list` | ✅ | ✅ admin | Lista de todas las reservas — **⚠️ bug: crashea** |
| `/orders/edit/<int>/` | `edit_order` | ✅ | ✅ admin | Editar reserva (admin) |
| `/orders/delete/<int>/` | `delete_order` | ✅ | ✅ admin | Eliminar reserva (admin) |

### Bug en `order_list` — `orders/views.py:308-312`

```python
@login_required
@user_passes_test(lambda u: u.is_admin)
def order_list(request):
    paginator = Paginator(order_list, 10)  # ← order_list es la función misma, no un queryset!
    page_number = request.GET.get('page')
    orders = Order.objects.filter(is_ordered=1)
    return render(request, 'order_list.html', {'orders': orders})
```

La línea `paginator = Paginator(order_list, 10)` pasa la función `order_list` como primer argumento (en lugar de un queryset). Esto producirá un `TypeError` en tiempo de ejecución cuando se acceda a `/orders/reservas/`.

### Template faltante

**`place_order`** renderiza `'orders/place_order.html'` — este template **no existe** en el directorio de templates. Si el formulario GET llega a `place_order`, se producirá `TemplateDoesNotExist`.

---

## Vista de home — `ecommerce/views.py`

**`home(request)`** — devuelve todos los productos ordenados por `created_date` con sus reseñas activas. La línea de filtro `is_available=True` está comentada (`#products = Product.objects.all().filter(...)`).

---

[← Volver al índice](00_INDICE.md)
