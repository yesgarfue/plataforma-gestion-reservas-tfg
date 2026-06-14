---
run_id: run_2026-05-11_13-11
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-11T13:26:50+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-11_13-11`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale español.
- Backend de correo configurable (console para desarrollo, SMTP para producción).
- Datos seed idempotentes (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, 1 admin, 1 cliente).
- Docker para empaquetado y despliegue.
- Seguridad mínima: contraseñas hasheadas, CSRF activo, validación de formularios.

## Apps Django

### accounts

**Propósito**: Gestionar autenticación, registro, login, logout y perfil de usuario cliente.

**Archivos principales**

- accounts/models.py
- accounts/forms.py
- accounts/views.py
- accounts/urls.py
- templates/accounts/register.html
- templates/accounts/login.html
- templates/accounts/profile.html

### catalog

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda, filtros y ficha detallada.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/filters.py
- templates/catalog/barco_list.html
- templates/catalog/barco_detail.html

### cart

**Propósito**: Gestionar cesta de compra, persistencia en sesión, modificación de cantidades y vaciado.

**Archivos principales**

- cart/models.py
- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/cart_detail.html

### reservations

**Propósito**: Gestionar reservas en tres pasos, estados, pago PayPal, contra-reembolso, seguimiento por código y correos.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/paypal.py
- reservations/services/email.py
- reservations/management/commands/send_payment_reminders.py
- templates/reservations/checkout_step1.html
- templates/reservations/checkout_step2.html
- templates/reservations/checkout_step3.html
- templates/reservations/tracking.html

### admin_panel

**Propósito**: Gestionar barcos, clientes y reservas desde panel administrativo con restricciones de negocio.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/barco_list.html
- templates/admin_panel/barco_form.html
- templates/admin_panel/cliente_list.html
- templates/admin_panel/reserva_list.html
- templates/admin_panel/reserva_detail.html

### core

**Propósito**: Configuración central, datos seed, utilidades y comandos de inicialización.

**Archivos principales**

- core/management/commands/seed_data.py
- core/utils.py
- core/settings.py

## Modelos

### Categoria

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120, unique=True)
- descripcion: TextField(blank=True)

### Puerto

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120, unique=True)
- ubicacion: CharField(max_length=255, blank=True)

### Fabricante

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120, unique=True)
- pais: CharField(max_length=120, blank=True)

### Barco

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120)
- categoria: ForeignKey(Categoria, on_delete=PROTECT)
- puerto: ForeignKey(Puerto, on_delete=PROTECT)
- fabricante: ForeignKey(Fabricante, on_delete=PROTECT)
- precio_dia: DecimalField(max_digits=8, decimal_places=2)
- capacidad: PositiveIntegerField
- imagen: ImageField(upload_to=barcos/, blank=True)
- disponible: BooleanField(default=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- email_contacto: EmailField
- nombre_contacto: CharField(max_length=120)
- telefono_contacto: CharField(max_length=20)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- importe_combustible: DecimalField(max_digits=8, decimal_places=2, default=0)
- fecha_inicio: DateField
- fecha_fin: DateField
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE, related_name=lineas)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)
- subtotal: DecimalField(max_digits=10, decimal_places=2)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | home | GET | public | HomeView |
| /registro/ | accounts:register | GET\|POST | public | RegisterView |
| /login/ | accounts:login | GET\|POST | public | LoginView |
| /logout/ | accounts:logout | POST | login_required | LogoutView |
| /perfil/ | accounts:profile | GET | login_required | ProfileView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /cesta/ | cart:cart_detail | GET | public | CartDetailView |
| /cesta/anadir/ | cart:add_to_cart | POST | public | AddToCartView |
| /cesta/actualizar/ | cart:update_cart | POST | public | UpdateCartView |
| /cesta/vaciar/ | cart:clear_cart | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:checkout_step1 | GET\|POST | public | CheckoutStep1View |
| /reserva/paso2/ | reservations:checkout_step2 | GET\|POST | public | CheckoutStep2View |
| /reserva/paso3/ | reservations:checkout_step3 | GET\|POST | public | CheckoutStep3View |
| /reserva/paypal/return/ | reservations:paypal_return | GET | public | PayPalReturnView |
| /reserva/paypal/cancel/ | reservations:paypal_cancel | GET | public | PayPalCancelView |
| /seguimiento/ | reservations:tracking | GET\|POST | public | TrackingView |
| /mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /reserva/<int:id>/cancelar/ | reservations:cancel_reservation | POST | login_required | CancelReservationView |
| /admin/ | admin:dashboard | GET | admin_required | AdminDashboardView |
| /admin/barcos/ | admin:barco_list | GET | admin_required | AdminBarcoListView |
| /admin/barcos/crear/ | admin:barco_create | GET\|POST | admin_required | AdminBarcoCreateView |
| /admin/barcos/<int:id>/editar/ | admin:barco_edit | GET\|POST | admin_required | AdminBarcoEditView |
| /admin/barcos/<int:id>/eliminar/ | admin:barco_delete | POST | admin_required | AdminBarcoDeleteView |
| /admin/clientes/ | admin:cliente_list | GET | admin_required | AdminClienteListView |
| /admin/clientes/<int:id>/eliminar/ | admin:cliente_delete | POST | admin_required | AdminClienteDeleteView |
| /admin/reservas/ | admin:reserva_list | GET | admin_required | AdminReservaListView |
| /admin/reservas/<int:id>/ | admin:reserva_detail | GET\|POST | admin_required | AdminReservaDetailView |
