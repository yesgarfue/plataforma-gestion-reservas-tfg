# 10 — Seguridad

[← Volver al índice](00_INDICE.md)

---

## Resumen de hallazgos

| # | Severidad | Título | Archivo | Línea |
|---|---|---|---|---|
| S-01 | **CRÍTICA** | SECRET_KEY inválida hardcodeada | `settings.py` | 25 |
| S-02 | **CRÍTICA** | Contraseña SMTP hardcodeada | `settings.py` | 32 |
| S-03 | **CRÍTICA** | Endpoint de eliminación de usuario sin autenticación | `accounts/views.py` | 431 |
| S-04 | **ALTA** | DEBUG=True en producción | `settings.py` | 36 |
| S-05 | **ALTA** | Cliente PayPal hardcodeado en template público | `templates/base.html` | 33 |
| S-06 | **ALTA** | Bug en order_list: NameError en producción | `orders/views.py` | 309 |
| S-07 | **ALTA** | db.sqlite3 versionado en el repositorio | raíz del repo | — |
| S-08 | **MEDIA** | jQuery 2.0.0 con vulnerabilidades conocidas | `static/js/` | — |
| S-09 | **MEDIA** | Redirección abierta vía parámetro `next` | `accounts/views.py` | 117 |
| S-10 | **MEDIA** | Sin rate limiting en login | `accounts/views.py` | 67 |
| S-11 | **MEDIA** | Hash de contraseña expuesto en formulario HTML | `accounts/forms.py` | 37-39 |
| S-12 | **MEDIA** | CORS configurado pero sin middleware instalado | `settings.py` | 163 |
| S-13 | **MEDIA** | Imagen de perfil default inexistente | `accounts/views.py` | 43 |
| S-14 | **BAJA** | except vacío (`pass`) en carts | `carts/views.py` | 136 |
| S-15 | **BAJA** | SESSION_TIMEOUT_REDIRECT sin barra inicial | `settings.py` | 72 |
| S-16 | **BAJA** | `django.contrib.sites` no en INSTALLED_APPS | `settings.py` | 44 |
| S-17 | **BAJA** | custom.css cargado dos veces | `templates/base.html` | 26, 28 |

---

## Detalle por hallazgo

### S-01 — CRÍTICA: SECRET_KEY inválida

**Archivo:** `ecommerce/settings.py:25`

```python
SECRET_KEY = 1234
```

Problemas:
1. Es un entero, no un string — Django 3.2 acepta cualquier valor pero lo usa como string, resultando en una clave trivialmente predecible.
2. Es hardcodeada en el repositorio.
3. Con la SECRET_KEY comprometida, un atacante puede falsificar cookies de sesión, tokens CSRF y cualquier firma criptográfica de Django.

**Corrección:**
```python
# .env
SECRET_KEY=django-insecure-<cadena-aleatoria-50-chars>

# settings.py
from decouple import config
SECRET_KEY = config('SECRET_KEY')
```

---

### S-02 — CRÍTICA: Contraseña SMTP hardcodeada

**Archivo:** `ecommerce/settings.py:32`

```python
EMAIL_HOST_PASSWORD = '<CREDENCIAL_RETIRADA>'
```

La contraseña de aplicación de Google estuvo expuesta en el código original. El valor fue retirado de los materiales publicados y la credencial debe permanecer revocada.

**Corrección:** Revocar inmediatamente la contraseña en la cuenta de Google y regenerarla. Mover a variable de entorno.

---

### S-03 — CRÍTICA: Endpoint de eliminación sin autenticación

**Archivo:** `accounts/views.py:431`

```python
def delete_user(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    # Sin @login_required ni @user_passes_test
    ...
    user.delete()
```

Cualquier visitante no autenticado puede enviar una petición GET a `/accounts/delete_user/1/` y eliminar cualquier usuario de la base de datos, incluyendo administradores.

**Corrección:**
```python
@login_required
@user_passes_test(lambda u: u.is_admin)
def delete_user(request, user_id):
    ...
```

---

### S-04 — ALTA: DEBUG=True en producción

**Archivo:** `ecommerce/settings.py:36`

Con `DEBUG=True` y el sitio desplegado en Render, cualquier error 500 muestra la traza de Python completa con variables locales. Esto puede exponer la configuración (incluidos los secretos), rutas del servidor y lógica interna.

**Corrección:** `DEBUG = config('DEBUG', default=False, cast=bool)` y asegurarse de que la variable de entorno en Render sea `DEBUG=False`.

---

### S-05 — ALTA: Client ID de PayPal expuesto

**Archivo:** `templates/base.html:33`

```html
<script src="https://www.paypal.com/sdk/js?client-id=AcR7zkd...J2jQ&currency=EUR"></script>
```

El client-id de PayPal de producción está hardcodeado en el template (visible en el HTML fuente de todas las páginas). Aunque PayPal diseña los client-ids para ser públicos, expone el identificador de la cuenta de negocio, lo que puede ser útil para ataques de ingeniería social o abuso de la API.

**Corrección:** Cargar desde variable de entorno e inyectar al template vía contexto o `{% if settings.PAYPAL_CLIENT_ID %}`.

---

### S-06 — ALTA: Bug que crashea order_list

**Archivo:** `orders/views.py:309`

```python
def order_list(request):
    paginator = Paginator(order_list, 10)  # ← order_list es la función, no un queryset
```

Acceder a `/orders/reservas/` lanzará `TypeError: object of type 'function' has no len()`. La vista de administración de reservas está rota.

**Corrección:**
```python
orders_qs = Order.objects.filter(is_ordered=True).order_by('-created_at')
paginator = Paginator(orders_qs, 10)
```

---

### S-07 — ALTA: db.sqlite3 en el repositorio

El archivo `db.sqlite3` está incluido en el repositorio git. Contiene datos reales de prueba (usuarios con emails, reservas, contraseñas hasheadas). Aunque las contraseñas están hasheadas, los datos personales están expuestos.

**Corrección:** Añadir `db.sqlite3` al `.gitignore` y eliminar del historial con `git filter-branch` o `git-filter-repo`.

---

### S-08 — MEDIA: jQuery 2.0.0

**Archivo:** `static/js/jquery-2.0.0.min.js`

jQuery 2.0.0 es de 2013 y tiene múltiples CVEs conocidos (XSS via `.html()`, `.append()`, etc.). La versión actual es 3.7+.

**Corrección:** Actualizar a jQuery 3.7.x mínimo.

---

### S-09 — MEDIA: Redirección abierta

**Archivo:** `accounts/views.py:117`

```python
next_url = request.POST.get('next') or request.GET.get('next') or 'home'
return redirect(next_url)
```

Si `next` contiene una URL absoluta externa (`https://evil.com`), Django redirigirá al usuario fuera del sitio tras el login (open redirect). Esto puede usarse en ataques de phishing.

**Corrección:**
```python
from django.utils.http import url_has_allowed_host_and_scheme
next_url = request.POST.get('next') or request.GET.get('next') or 'home'
if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
    next_url = 'home'
return redirect(next_url)
```

---

### S-10 — MEDIA: Sin rate limiting en login

**Archivo:** `accounts/views.py:67`

No hay ningún mecanismo que limite los intentos de login (no hay CAPTCHA, no hay bloqueo de cuenta, no hay throttling). El endpoint `/accounts/login/` es vulnerable a ataques de fuerza bruta.

**Corrección:** Implementar `django-axes` o `django-ratelimit` para limitar intentos por IP/usuario.

---

### S-11 — MEDIA: Hash de contraseña expuesto en formulario

**Archivo:** `accounts/forms.py:37-39`

```python
if self.instance and self.instance.pk:
    self.fields['password'].widget.attrs['readonly'] = True
    self.fields['password'].widget.attrs['value'] = self.instance.password  # Hash expuesto
```

En el formulario de edición de usuario (`/accounts/edit_user/<id>/`), el hash bcrypt de la contraseña se renderiza como valor del input HTML. El hash es visible en el código fuente de la página para cualquier administrador autenticado (y potencialmente en proxies o logs).

**Corrección:** Excluir los campos de contraseña del formulario de edición. Usar un formulario separado para cambio de contraseña.

---

### S-12 — MEDIA: CORS configurado sin middleware

**Archivo:** `ecommerce/settings.py:163-165`

```python
CORS_ALLOWED_ORIGINS = ["https://www.paypal.com"]
```

El middleware `corsheaders.middleware.CorsMiddleware` no está instalado (ni en `requirements.txt` ni en `INSTALLED_APPS`). Este setting no tiene ningún efecto. No hay protección CORS real.

---

### S-13 — MEDIA: Imagen de perfil por defecto inexistente

**Archivo:** `accounts/views.py:43`

```python
profile.profile_picture = 'default/default-user.png'
```

El directorio `media/default/` no existe. Cualquier template que intente renderizar la imagen de perfil de un usuario recién registrado obtendrá un error 404 o link roto.

---

### S-14 — BAJA: except vacío oculta errores

**Archivo:** `carts/views.py:136`

```python
try:
    ...
except:
    pass
```

Un `except` sin tipo captura todo incluyendo `KeyboardInterrupt` y `SystemExit`. Oculta errores silenciosamente. Usar `except Exception` como mínimo y logear el error.

---

### S-15 — BAJA: SESSION_TIMEOUT_REDIRECT relativo

**Archivo:** `ecommerce/settings.py:72`

```python
SESSION_TIMEOUT_REDIRECT = 'accounts/login'
```

Sin barra inicial (`/`) puede generar redirecciones relativas incorrectas dependiendo de la URL actual cuando expira la sesión. Debería ser `'/accounts/login/'`.

---

### S-16 — BAJA: django.contrib.sites ausente

`get_current_site(request)` se usa en `accounts/views.py` y `orders/views.py` para construir URLs de email. En Django 3.2, esto funciona sin `django.contrib.sites` en INSTALLED_APPS gracias a compatibilidad interna, pero es técnicamente incorrecto y podría producir URLs incorrectas.

---

### S-17 — BAJA: CSS duplicado en base.html

**Archivo:** `templates/base.html:26, 28`

`custom.css` se carga dos veces. No es un riesgo de seguridad pero añade latencia innecesaria.

---

[← Volver al índice](00_INDICE.md)
