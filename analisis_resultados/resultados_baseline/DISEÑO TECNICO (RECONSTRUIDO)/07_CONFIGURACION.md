# 07 — Configuración

[← Volver al índice](00_INDICE.md)

---

## Archivo de configuración

`ecommerce/settings.py` — única configuración, sin separación dev/prod.

---

## DEBUG y ALLOWED_HOSTS

```python
# settings.py:36-38
DEBUG = True

ALLOWED_HOSTS = [
    'alquiler-de-barcos.onrender.com',
    'localhost',
    'pgpi-g3-2.onrender.com',
    '127.0.0.1'
]
```

**⚠️ `DEBUG = True` en producción** — la aplicación está desplegada en Render con debug activo. Esto expone trazas de error completas (incluyendo variables locales) a cualquier visitante en caso de error.

---

## INSTALLED_APPS

```python
# settings.py:44-56
INSTALLED_APPS = [
    'django.contrib.admin',          # Panel admin Django
    'django.contrib.auth',           # Sistema auth base
    'django.contrib.contenttypes',   # Framework de content types
    'django.contrib.sessions',       # Gestión de sesiones
    'django.contrib.messages',       # Mensajes flash
    'django.contrib.staticfiles',    # Servicio de estáticos
    'category',                      # Categorías de barcos
    'accounts',                      # Usuarios personalizados
    'store',                         # Catálogo de barcos
    'carts',                         # Carrito de reservas
    'orders',                        # Pedidos y pagos
]
```

**Ausentes notables:**

| Librería | En requirements.txt | En INSTALLED_APPS | Problema |
|---|---|---|---|
| `django-admin-honeypot` | Sí (`1.1.0`) | **No** | Librería pagada/instalada sin efecto |
| `django-ckeditor` | Sí (`6.2.0`) | **No** | Librería instalada sin uso |
| `django.contrib.sites` | (built-in) | **No** | `get_current_site()` se usa en múltiples vistas — puede funcionar por compat legacy pero es técnicamente incorrecto |

---

## MIDDLEWARE

```python
# settings.py:58-67
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Headers de seguridad
    'django.contrib.sessions.middleware.SessionMiddleware',   # Sesiones
    'django.middleware.common.CommonMiddleware',              # Normalizaciones HTTP
    'django.middleware.csrf.CsrfViewMiddleware',              # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Usuario autenticado en request
    'django.contrib.messages.middleware.MessageMiddleware',   # Mensajes flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # X-Frame-Options
    'django_session_timeout.middleware.SessionTimeoutMiddleware', # Expiración de sesión 30min
]
```

**Ausente:** `corsheaders.middleware.CorsMiddleware` — el setting `CORS_ALLOWED_ORIGINS` está configurado (`settings.py:163-165`) pero el middleware correspondiente (`django-cors-headers`) ni está instalado ni en `requirements.txt`.

---

## Estáticos y Media

```python
# settings.py:135-142
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')      # Destino de collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'ecommerce/static')       # Fuente de desarrollo
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Los archivos media se sirven en desarrollo mediante `static(settings.MEDIA_URL, ...)` añadido en `ecommerce/urls.py:30`. En producción (Render) no hay configuración de servicio de media files (S3, Cloudinary, etc.).

---

## Seguridad de cookies y CSRF

```python
# settings.py:158-161
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
```

`SameSite=None` + `Secure=True` permite enviar las cookies en peticiones cross-site (necesario para el flujo de PayPal). Sin embargo, en desarrollo (`DEBUG=True`, HTTP sin TLS), `Secure=True` puede causar que las cookies no se envíen y romper la sesión. Este es un ajuste de producción mezclado con configuración de desarrollo.

---

## Configuración de email SMTP

```python
# settings.py:27-33
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hundidosgestion@gmail.com'
EMAIL_HOST_PASSWORD = '<CREDENCIAL_RETIRADA>'
DEFAULT_FROM_EMAIL = 'hundidosgestion@gmail.com'
```

---

## ⚠️ SECRETOS HARDCODEADOS

| Secreto | Archivo | Línea | Severidad |
|---|---|---|---|
| `SECRET_KEY = 1234` | `ecommerce/settings.py` | 25 | **CRÍTICA** — valor numérico (ni siquiera es string), no es una clave secreta válida |
| `EMAIL_HOST_PASSWORD` | `ecommerce/settings.py` | 32 | **ALTA** — la credencial original fue retirada y debe rotarse |
| PayPal client-id (`AcR7zk...J2jQ`) | `templates/base.html` | 33 | **MEDIA** — client ID de PayPal producción expuesto en HTML público (aunque no es secreto técnicamente, permite crear pagos en nombre de la cuenta) |

La librería `python-decouple` está instalada y **ya importada** (`from decouple import config` en `settings.py:14`) pero **nunca se usa**. Todos los secretos deberían estar en un archivo `.env` y cargarse con `config('SECRET_KEY')`, `config('EMAIL_HOST_PASSWORD')`, etc.

---

## Otras configuraciones

```python
# settings.py:123-129
LANGUAGE_CODE = 'es'      # Español
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# settings.py:156
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py:146-149
MESSAGE_TAGS = {messages.ERROR: 'danger'}   # Mapea ERROR → clase CSS 'danger' de Bootstrap

# settings.py:70-72
SESSION_EXPIRE_SECONDS = 1800               # Sesión expira a los 30 min de inactividad
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = 'accounts/login' # Sin barra inicial — puede redirigir a URL relativa incorrecta

# settings.py:163-165
CORS_ALLOWED_ORIGINS = ["https://www.paypal.com"]  # Sin middleware instalado — sin efecto
```

---

## Inconsistencia de versión Django en settings

El comentario generado automáticamente en `settings.py:1-11` dice:
```
Generated by 'django-admin startproject' using Django 4.2.2.
```

Pero `requirements.txt:3` especifica `Django==3.2.20`. La versión instalada y ejecutada es **3.2.20**.

---

[← Volver al índice](00_INDICE.md)
