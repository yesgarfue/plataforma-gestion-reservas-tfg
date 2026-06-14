# 02 — Arquitectura del Proyecto

[← Volver al índice](00_INDICE.md)

---

## Árbol de carpetas comentado

```
hundidos/                          ← Raíz del proyecto
│
├── ecommerce/                     ← Paquete de configuración del proyecto Django
│   ├── settings.py                ← Configuración global (BD, apps, middleware, email...)
│   ├── urls.py                    ← Enrutador raíz
│   ├── views.py                   ← Vista única: home()
│   ├── wsgi.py                    ← Punto de entrada WSGI
│   ├── asgi.py                    ← Punto de entrada ASGI (no configurado)
│   └── static/                    ← Estáticos del proyecto (CSS, JS, fonts, imágenes)
│       ├── css/                   ← Bootstrap, custom.css, responsive.css, ui.css
│       ├── js/                    ← jQuery 2.0.0, Bootstrap bundle, script.js
│       ├── fonts/                 ← FontAwesome (local), Roboto
│       └── images/                ← Favicon, iconos de pago, logos
│
├── accounts/                      ← App de usuarios y autenticación
│   ├── models.py                  ← Modelos Account y UserProfile
│   ├── views.py                   ← Register, login, logout, dashboard, perfil, admin de usuarios
│   ├── forms.py                   ← RegistrationForm, UserForm, UserProfileForm
│   ├── urls.py                    ← URLs de la app
│   ├── validators.py              ← CustomPasswordValidator
│   ├── admin.py                   ← AccountAdmin (extiende UserAdmin) + UserProfileAdmin; registra Account y UserProfile
│   └── migrations/                ← 6 migraciones
│
├── category/                      ← App de categorías de barcos
│   ├── models.py                  ← Modelo Category
│   ├── context_processors.py      ← Inyecta categorías al contexto global (menú)
│   ├── views.py                   ← (vacío)
│   ├── admin.py
│   └── migrations/                ← 3 migraciones
│
├── store/                         ← App principal del catálogo (barcos)
│   ├── models.py                  ← Puerto, Fabricante, Product, Variation, ReviewRating
│   ├── views.py                   ← Listado, detalle, búsqueda, reseñas, CRUD admin de barcos
│   ├── forms.py                   ← ReviewForm, ProductForm
│   ├── urls.py                    ← URLs de la app
│   ├── admin.py                   ← ProductAdmin, VariationAdmin, ReviewRating
│   └── migrations/                ← 5 migraciones
│
├── carts/                         ← App del carrito de reservas
│   ├── models.py                  ← Cart, CartItem (con fechas de reserva)
│   ├── views.py                   ← add_cart, remove_cart, cart, checkout, update_cart
│   ├── context_processors.py      ← Inyecta cart_count al contexto global (navbar)
│   ├── urls.py                    ← URLs de la app
│   └── migrations/                ← 6 migraciones
│
├── orders/                        ← App de pedidos/reservas
│   ├── models.py                  ← Payment, Order, OrderProduct (con fechas de reserva)
│   ├── views.py                   ← place_order, payments, order_complete, mark_pending, CRUD admin
│   ├── forms.py                   ← OrderForm, OrderAdminForm
│   ├── urls.py                    ← URLs de la app
│   ├── admin.py                   ← OrderAdmin + OrderProductInline (inline); Payment registrado sin clase personalizada
│   └── migrations/                ← 10 migraciones
│
├── templates/                     ← Plantillas HTML globales
│   ├── base.html                  ← Plantilla base (extienden todas las demás)
│   ├── home.html                  ← Página principal
│   ├── list_users.html            ← Lista de usuarios (admin)
│   ├── order_list.html            ← Lista de reservas (admin)
│   ├── product_list.html          ← Lista de barcos (admin)
│   ├── accounts/                  ← Plantillas de autenticación y perfil
│   ├── includes/                  ← Fragmentos reutilizables (navbar, footer, alerts, sidebar)
│   ├── orders/                    ← Plantillas de checkout y confirmación
│   └── store/                     ← Plantillas del catálogo y carrito
│
├── static/                        ← Colectados por collectstatic (réplica de ecommerce/static/)
├── media/                         ← Archivos subidos (imágenes de barcos, fotos de perfil)
│
├── db.sqlite3                     ← Base de datos SQLite (incluida en el repositorio)
├── manage.py                      ← Herramienta de gestión Django
├── requirements.txt               ← Dependencias Python
├── Dockerfile                     ← Imagen Docker
└── docker-compose.yml             ← Orquestación Docker
```

---

## Apps Django

| App | Descripción |
|---|---|
| `django.contrib.admin` | Panel de administración de Django |
| `django.contrib.auth` | Sistema base de autenticación (extendido por `accounts`) |
| `django.contrib.contenttypes` | Framework de tipos de contenido |
| `django.contrib.sessions` | Gestión de sesiones |
| `django.contrib.messages` | Framework de mensajes flash |
| `django.contrib.staticfiles` | Servicio de archivos estáticos |
| **`category`** | Categorías de barcos (Veleros, Yates, etc.) para navegación y filtros |
| **`accounts`** | Modelo de usuario personalizado, registro, login, recuperación de contraseña, perfiles |
| **`store`** | Catálogo de barcos, filtros de búsqueda, disponibilidad, reseñas, CRUD de admin |
| **`carts`** | Carrito de reservas con fechas de inicio/fin, cálculo de subtotales |
| **`orders`** | Proceso de checkout, pagos (PayPal + contra-reembolso), historial de reservas |

---

## Diagrama de dependencias entre apps

```
ecommerce (proyecto)
    │
    ├──▶ category          ← no depende de otras apps
    │
    ├──▶ accounts          ← no depende de otras apps de negocio
    │
    ├──▶ store
    │       ├── depende de ──▶ category (ForeignKey Product→Category)
    │       └── depende de ──▶ accounts (ForeignKey ReviewRating→Account)
    │
    ├──▶ carts
    │       ├── depende de ──▶ store (ForeignKey CartItem→Product, ManyToMany →Variation)
    │       └── depende de ──▶ accounts (ForeignKey CartItem→Account)
    │
    └──▶ orders
            ├── depende de ──▶ accounts (ForeignKey Order/Payment/OrderProduct→Account)
            ├── depende de ──▶ store (ForeignKey OrderProduct→Product, M2M →Variation)
            └── depende de ──▶ carts (importa CartItem en views para vaciar carrito)
```

La app `ecommerce/views.py` importa directamente de `store` (modelos `Product` y `ReviewRating`) para la vista `home`.

---

[← Volver al índice](00_INDICE.md)
