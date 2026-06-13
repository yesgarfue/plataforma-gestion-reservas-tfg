# 09 — Deuda Técnica

[← Volver al índice](00_INDICE.md)

---

## 1. Modelos duplicados

**Archivo:** `store/models.py:8-43`

Los modelos `Puerto` y `Fabricante` están definidos **dos veces** en el mismo archivo. La primera definición (líneas 8-26) es completa; la segunda (líneas 30-43) la sobreescribe. Python no lanza error porque la segunda definición simplemente reemplaza la primera en el namespace del módulo. El código funciona, pero es confuso y propenso a introducir divergencias.

```python
# Primera definición — líneas 8-26 (ignorada por Python)
class Puerto(models.Model): ...
class Fabricante(models.Model): ...

# Segunda definición — líneas 30-43 (la que realmente se usa)
class Puerto(models.Model): ...
class Fabricante(models.Model): ...
```

---

## 2. Imports no usados

| Archivo | Import | Línea | Motivo |
|---|---|---|---|
| `ecommerce/settings.py` | `from pathlib import Path` | 13 | `Path` no se usa; `BASE_DIR` se construye con `os.path` |
| `ecommerce/settings.py` | `from decouple import config` | 14 | `config()` no se llama en ningún punto del archivo |
| `accounts/views.py` | `from django.contrib.auth.models import User` | 19 | El modelo de usuario es `accounts.Account`; `User` nunca se usa |
| `accounts/views.py` | `import requests` | 18 | No hay ninguna llamada a `requests` en el archivo |
| `store/views.py` | `from .models import Product, Fabricante, Puerto` | 18 | Duplica el import de la línea 3; importados dos veces |
| `orders/views.py` | `from django.shortcuts import render, redirect, get_object_or_404` | 11 | Duplica la línea 3 |
| `orders/views.py` | `from django.contrib.auth.decorators import login_required` | 21 y 26 | Duplican la primera ocurrencia en línea 13 |
| `orders/views.py` | `from django.http import JsonResponse` | 23 | Duplica la línea 4 |
| `orders/views.py` | `from django.contrib import messages` | 28 | Duplica la línea 22 |
| `orders/views.py` | `from store.models import Product` | 16 | Duplica la línea 9 (además añade `Variation`) |
| `orders/models.py` | `# from jsonschema import ValidationError` | 4 | Comentado — nunca llegó a usarse |
| `store/admin.py` | `import admin_thumbnails` | 3 | Importado pero el decorador `@admin_thumbnails.thumbnail` no se aplica a ningún modelo |

---

## 3. Dependencias en requirements.txt sin uso en el código

| Librería | Versión | Estado |
|---|---|---|
| `django-admin-honeypot` | 1.1.0 | No está en `INSTALLED_APPS`; sin efecto |
| `django-ckeditor` | 6.2.0 | No está en `INSTALLED_APPS`; ningún campo `RichTextField` en ningún modelo |
| `playwright` | sin pin | No hay tests que lo usen (los archivos `tests.py` están vacíos) |
| `selenium` | sin pin | No hay tests que lo usen (los archivos `tests.py` están vacíos) |
| `python-decouple` | 3.8 | Importado en settings.py pero `config()` nunca se llama |
| `requests` | 2.27.1 | Importado en `accounts/views.py` pero sin ninguna llamada |

---

## 4. Función duplicada: `_cart_id`

La función `_cart_id(request)` (que devuelve `request.session.session_key`) está definida dos veces:
- `carts/views.py:12-15`
- `orders/views.py:36-40`

Son idénticas. La de `orders/views.py` nunca se usa dentro de ese módulo (se usa la importada de `carts.views`).

---

## 5. Archivos `tests.py` vacíos

Los 5 apps (`accounts`, `category`, `store`, `carts`, `orders`) tienen archivos `tests.py` que solo contienen `from django.test import TestCase`. No hay ningún test escrito a pesar de que `playwright` y `selenium` están en `requirements.txt`, lo que sugiere intención de testing nunca materializada.

---

## 6. Código comentado / comentarios de desarrollo

| Archivo | Línea | Contenido |
|---|---|---|
| `ecommerce/views.py:5` | — | `#products = Product.objects.all().filter(is_available=True).order_by('created_date')` — filtro desactivado |
| `ecommerce/views.py:11` | — | `#reviews = ReviewRating.objects.filter(product_id=product.id, status=True)` |
| `ecommerce/views.py:17` | — | `#'reviews': reviews,` — en el contexto |
| `orders/models.py:4` | — | `# from jsonschema import ValidationError` — import comentado sin propósito |
| `orders/views.py:85` | — | `#Copiar las variaciones` — comentario de desarrollo |
| `orders/views.py:246` | — | `# Marca como PENDIENTE DE PAGO si la reserva no se ha pagado (opcion contra reembolso)` — comentario aclaratorio aceptable |
| `orders/models.py:43` | — | `# Estados de una reserva` |
| `orders/models.py:41` | — | `state = models.CharField(max_length=5) # QUE ES CODIGO POSTAL EN CHECKOUT.HTML` — comentario de desarrollo que no debería estar en producción |

---

## 7. TODO / FIXME encontrados

No se encontraron comentarios explícitos `# TODO` o `# FIXME` en el código fuente. Los problemas pendientes están implícitos en código comentado y notas inline.

---

## 8. Residuos de la plantilla e-commerce original

Estos elementos no tienen relación con "alquiler de barcos" y provienen de la plantilla de e-commerce original:

| Elemento | Archivo | Por qué es residuo |
|---|---|---|
| `Variation` model (color/talla) | `store/models.py` | Las variaciones de color y talla son para ropa/productos; no aplican a alquiler de barcos |
| `VariationManager` con `colors()` y `tallas()` | `store/models.py` | Mismo motivo |
| `CartItem.variation` (ManyToMany Variation) | `carts/models.py` | La lógica de variaciones en el carrito no aporta nada al flujo de reserva |
| `OrderProduct.variation` (ManyToMany) | `orders/models.py` | Ídem — se copia la variación pero no se usa en templates ni lógica de negocio |
| `media/images/banners/blackfriday.png` | `media/` | Banner de Black Friday, concepto de e-commerce de productos, no de alquiler |
| `media/photos/products/OIP_1.jfif` (y variantes) | `media/photos/products/` | Imágenes de placeholder del e-commerce original (`OIP` = imágenes de Bing) |
| `ecommerce/static/images/misc/cash.jpg` | `static/images/misc/` | Imagen de "pago en efectivo" de la plantilla |
| Nombre del paquete `ecommerce/` | `ecommerce/settings.py` | El proyecto se llama "hundidos" pero el paquete de configuración sigue llamándose `ecommerce` |

---

## 9. Bugs funcionales identificados

| Bug | Archivo | Línea | Descripción |
|---|---|---|---|
| `order_list` crashea | `orders/views.py` | 309 | `Paginator(order_list, 10)` pasa la función como argumento en vez de un queryset |
| Template inexistente | `orders/views.py` | 214 | `render(request, 'orders/place_order.html', ...)` — el template no existe |
| `delete_user` sin auth | `accounts/views.py` | 431 | Sin `@login_required` ni `@user_passes_test` |
| `submit_review` sin auth | `store/views.py` | 205 | Sin `@login_required`; si no hay usuario, `request.user.id` es None |
| Imagen de perfil default | `accounts/views.py` | 43 | `profile_picture = 'default/default-user.png'` — directorio `media/default/` no existe |
| `UserProfile` no creado al hacer login | `accounts/views.py` | 176 | `dashboard` llama `UserProfile.objects.get(user_id=...)` sin protección; si el perfil no existe (usuario creado por admin sin perfil) lanza `ObjectDoesNotExist` sin manejar |
| `__unicode__` en Python 3 | `carts/models.py` | 42 | `__unicode__` no se llama en Python 3; debería ser `__str__` |
| `last_login` nunca actualizado | `accounts/models.py` | 52 | Usa `auto_now_add` en lugar de actualizarse al hacer login |
| **`Order.status` default inválido** | `orders/models.py` | 48 | `default='New'` no está en las choices (`Pagado`, `Pendiente de pago`, `En uso`, `Devuelto`); cada pedido nuevo nace con un estado que ningún filtro ni template reconoce |
| `list_display_link` typo en AccountAdmin | `accounts/admin.py` | 9 | Debería ser `list_display_links` (con 's'); el atributo no tiene ningún efecto |

---

## 10. Archivos duplicados innecesarios

- `ecommerce/static/` y `static/` contienen los mismos archivos CSS/JS/fonts. La carpeta `static/` es el output de `collectstatic` y no debería estar versionada.
- `media/images/icons/` y `media/images/misc/` son duplicados de `ecommerce/static/images/icons/` y `ecommerce/static/images/misc/`.

---

[← Volver al índice](00_INDICE.md)
