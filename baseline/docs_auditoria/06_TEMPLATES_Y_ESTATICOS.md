# 06 — Templates y Estáticos

[← Volver al índice](00_INDICE.md)

---

## Jerarquía de templates

```
templates/
│
├── base.html                          ← Plantilla base global
│   ├── home.html                      ← extends base.html
│   ├── list_users.html                ← extends base.html
│   ├── order_list.html                ← extends base.html
│   ├── product_list.html              ← extends base.html
│   │
│   ├── accounts/
│   │   ├── register.html             ← extends base.html
│   │   ├── login.html                ← extends base.html
│   │   ├── dashboard.html            ← extends base.html
│   │   ├── edit_profile.html         ← extends base.html
│   │   ├── change_password.html      ← extends base.html
│   │   ├── forgotPassword.html       ← extends base.html
│   │   ├── resetPassword.html        ← extends base.html
│   │   ├── my_orders.html            ← extends base.html
│   │   ├── create_users.html         ← extends base.html
│   │   ├── edit_user.html            ← extends base.html
│   │   ├── account_verification_email.html  ← email (no extiende base.html)
│   │   └── reset_password_email.html        ← email (no extiende base.html)
│   │
│   ├── store/
│   │   ├── store.html                ← extends base.html
│   │   ├── product_detail.html       ← extends base.html
│   │   ├── cart.html                 ← extends base.html
│   │   ├── checkout.html             ← extends base.html
│   │   ├── create_ship.html          ← extends base.html
│   │   └── edit_ship.html            ← extends base.html
│   │
│   └── orders/
│       ├── payments.html             ← extends base.html
│       ├── order_complete.html       ← extends base.html
│       ├── order_incomplete.html     ← extends base.html
│       ├── order_not_found.html      ← extends base.html
│       ├── edit_order.html           ← extends base.html
│       ├── order_paid_email.html     ← email (no extiende base.html)
│       └── order_recieved_email.html ← email — **typo**: "recieved" en lugar de "received"
│
└── includes/
    ├── navbar.html                   ← {% include %} desde base.html
    ├── footer.html                   ← {% include %} desde base.html
    ├── alerts.html                   ← {% include %} desde templates individuales
    └── dashboard_sidebar.html        ← {% include %} desde dashboard.html
```

**Template faltante:** `orders/place_order.html` — referenciado en `orders/views.py:214` pero no existe.

---

## Template base — `templates/base.html`

Define la estructura HTML completa. Bloques disponibles:

| Bloque | Descripción |
|---|---|
| `{% block content %}` | Contenido principal de cada página |

Incluye:
- `{% include 'includes/navbar.html' %}`
- `{% include 'includes/footer.html' %}`
- jQuery 2.0.0 (local)
- Bootstrap 4 bundle (local)
- FontAwesome (local + CDN externo 4.7.0)
- FullCalendar 6.1.8 (CDN)
- PayPal JS SDK (CDN, client_id hardcodeado — **ver [10_SEGURIDAD.md](10_SEGURIDAD.md)**)
- custom.css cargado **dos veces** (líneas 26 y 28)

---

## Formularios — `forms.py` por app

### `accounts/forms.py`

| Formulario | Modelo | Campos | Validaciones |
|---|---|---|---|
| `RegistrationForm` | `Account` | first_name, last_name, phone_number, email, password, confirm_password, is_admin | Contraseñas coincidan; `validate_password()`; email único; username único derivado del email |
| `UserForm` | `Account` | first_name, last_name, phone_number | — |
| `UserProfileForm` | `UserProfile` | address_line_1, address_line_2, city, state, country, profile_picture | Solo archivos de imagen |

**Nota de seguridad:** `RegistrationForm` en modo edición pone la contraseña hasheada como `value` en el campo de contraseña (readonly). El hash queda expuesto en el HTML del formulario de edición de usuario.

### `store/forms.py`

| Formulario | Modelo | Campos | Validaciones |
|---|---|---|---|
| `ReviewForm` | `ReviewRating` | subject, review, rating | Hereda de ModelForm |
| `ProductForm` | `Product` | images, product_name, description, price, capacidad, stock, category, fabricante, puerto | capacidad > 0; price > 0; stock ≥ 0 |

### `orders/forms.py`

| Formulario | Modelo | Campos | Validaciones |
|---|---|---|---|
| `OrderForm` | `Order` | first_name, last_name, phone, email, address_line_1, address_line_2, country, city, state, order_note | Nombre/apellido requeridos; teléfono ≥9 dígitos; email válido (regex); código postal = 5 dígitos |
| `OrderAdminForm` | `Order` | first_name, last_name, phone, email, address_line_1, address_line_2, country, city, state, status | Ídem sin order_note |

---

## Archivos estáticos

Los estáticos están **duplicados** en dos ubicaciones:

| Ruta | Propósito |
|---|---|
| `ecommerce/static/` | Fuente de desarrollo — referenciada en `STATICFILES_DIRS` |
| `static/` | Destino de `collectstatic` — referenciada en `STATIC_ROOT` |

Ambas carpetas contienen los mismos archivos CSS/JS/fonts. La carpeta `static/` en el repositorio no debería estar bajo control de versiones (debería estar en `.gitignore`).

### CSS

| Archivo | Descripción |
|---|---|
| `static/css/bootstrap.css` | Bootstrap 4 |
| `static/css/custom.css` | Estilos propios de la aplicación |
| `static/css/ui.css` | Estilos de UI de la plantilla original |
| `static/css/responsive.css` | Media queries para responsividad |

### JavaScript

| Archivo | Descripción |
|---|---|
| `static/js/jquery-2.0.0.min.js` | jQuery 2.0.0 (2013) — versión muy antigua |
| `static/js/bootstrap.bundle.min.js` | Bootstrap 4 bundle |
| `static/js/script.js` | Lógica JS personalizada |

### Imágenes en `ecommerce/static/images/`

| Archivo | Descripción |
|---|---|
| `favicon2.ico` | Favicon del sitio |
| `logo3.png`, `logo4.png` | Logotipos |
| `icons/pay-*.png` | Iconos de métodos de pago |
| `misc/btn-paypal.png`, `cash.jpg`, `payment-*.png` | Imágenes de métodos de pago |

---

## Media (archivos subidos)

```
media/
├── images/barcos/1.jpg … 10.jpg    ← Fotos de barcos demo
├── images/banners/blackfriday.png  ← Banner de Black Friday — ⚠️ residuo e-commerce
├── images/icons/                   ← Duplicado de static/images/icons/
├── images/misc/                    ← Duplicado de static/images/misc/
├── photos/products/                ← Fotos de productos (OIP_1.jfif etc.)
└── userprofile/                    ← Foto de perfil de un usuario demo
```

El banner `blackfriday.png` en `media/images/banners/` es un residuo evidente de la plantilla e-commerce original (Black Friday no tiene relación con el alquiler de barcos).

Las subcarpetas `media/images/icons/` y `media/images/misc/` son duplicados exactos de las mismas carpetas en `static/images/`. Probablemente copiados allí accidentalmente.

---

[← Volver al índice](00_INDICE.md)
