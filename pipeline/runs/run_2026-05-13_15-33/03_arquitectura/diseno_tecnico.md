---
run_id: run_2026-05-13_15-33
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-13T15:51:56+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-13_15-33`

## Stack técnico

- Python 3.9+ con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo sin integración externa.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale es_ES.
- Backend de correo configurable (console en desarrollo, SMTP en producción).
- Datos seed precargados para pruebas de todas las funcionalidades.
- Docker para empaquetado y despliegue.
- Transacciones explícitas con aislamiento SERIALIZABLE para manejo de concurrencia en SQLite.

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

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda, filtros y ficha de producto.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/filters.py
- templates/catalog/list.html
- templates/catalog/detail.html

### cart

**Propósito**: Gestionar cesta de compra en sesión, modificación de cantidades y vaciado.

**Archivos principales**

- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/summary.html

### reservations

**Propósito**: Gestionar reservas en tres pasos, estados, pagos, seguimiento por código y correos de confirmación y recordatorio.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/paypal.py
- reservations/services/email.py
- reservations/services/pricing.py
- templates/reservations/checkout_step1.html
- templates/reservations/checkout_step2.html
- templates/reservations/checkout_step3.html
- templates/reservations/confirmation.html
- templates/reservations/track.html

### admin_panel

**Propósito**: Panel de administración para gestión de barcos, clientes, reservas y cambio de estados.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/boats_list.html
- templates/admin_panel/boats_form.html
- templates/admin_panel/clients_list.html
- templates/admin_panel/reservations_list.html
- templates/admin_panel/reservation_detail.html

### core

**Propósito**: Configuración central, utilidades, management commands para seed data y tareas programadas.

**Archivos principales**

- core/settings.py
- core/urls.py
- core/management/commands/seed_data.py
- core/management/commands/send_payment_reminders.py
- core/utils.py
- core/middleware.py

## Modelos

### Categoria

- **App**: catalog

**Campos**

- nombre: CharField(max_length=100, unique=True)
- descripcion: TextField(blank=True)

### Puerto

- **App**: catalog

**Campos**

- nombre: CharField(max_length=100, unique=True)
- ubicacion: CharField(max_length=200)

### Fabricante

- **App**: catalog

**Campos**

- nombre: CharField(max_length=100, unique=True)
- pais: CharField(max_length=100, blank=True)

### Barco

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120)
- imagen: ImageField(upload_to=barcos/)
- categoria: ForeignKey(Categoria, on_delete=PROTECT)
- puerto: ForeignKey(Puerto, on_delete=PROTECT)
- fabricante: ForeignKey(Fabricante, on_delete=PROTECT)
- capacidad: PositiveIntegerField
- precio_dia: DecimalField(max_digits=8, decimal_places=2)
- activo: BooleanField(default=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- nombre_cliente: CharField(max_length=120)
- email_cliente: EmailField
- telefono_cliente: CharField(max_length=20, blank=True)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- fecha_inicio: DateField
- fecha_fin: DateField
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)
- tasa_combustible_dia: DecimalField(max_digits=8, decimal_places=2)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- metodo_pago: CharField(choices=paypal/contra_reembolso)
- referencia_paypal: CharField(max_length=255, blank=True, null=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- precio_unitario: DecimalField(max_digits=8, decimal_places=2)
- subtotal: DecimalField(max_digits=10, decimal_places=2)

### HistorialEstadoReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- estado_anterior: CharField(max_length=50)
- estado_nuevo: CharField(max_length=50)
- cambio_por: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- fecha_cambio: DateTimeField(auto_now_add=True)
- notas: TextField(blank=True)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /registro/ | accounts:register | GET\|POST | public | RegisterView |
| /login/ | accounts:login | GET\|POST | public | LoginView |
| /logout/ | accounts:logout | POST | login_required | LogoutView |
| /cuenta/ | accounts:profile | GET | login_required | ProfileView |
| /cuenta/reservas/ | accounts:my_reservations | GET | login_required | MyReservationsView |
| /cesta/ | cart:summary | GET | public | CartSummaryView |
| /cesta/agregar/ | cart:add | POST | public | AddToCartView |
| /cesta/actualizar/ | cart:update | POST | public | UpdateCartView |
| /cesta/vaciar/ | cart:clear | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:checkout_step1 | GET\|POST | public | CheckoutStep1View |
| /reserva/paso2/ | reservations:checkout_step2 | GET\|POST | public | CheckoutStep2View |
| /reserva/paso3/ | reservations:checkout_step3 | GET\|POST | public | CheckoutStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ConfirmationView |
| /reserva/seguimiento/ | reservations:track | GET\|POST | public | TrackReservationView |
| /reserva/<int:id>/cancelar/ | reservations:cancel | POST | login_required | CancelReservationView |
| /paypal/return/ | reservations:paypal_return | GET | public | PayPalReturnView |
| /paypal/cancel/ | reservations:paypal_cancel | GET | public | PayPalCancelView |
| /admin/ | admin_panel:dashboard | GET | admin_required | AdminDashboardView |
| /admin/barcos/ | admin_panel:boats_list | GET | admin_required | AdminBoatsListView |
| /admin/barcos/crear/ | admin_panel:boat_create | GET\|POST | admin_required | AdminBoatCreateView |
| /admin/barcos/<int:id>/editar/ | admin_panel:boat_edit | GET\|POST | admin_required | AdminBoatEditView |
| /admin/barcos/<int:id>/eliminar/ | admin_panel:boat_delete | POST | admin_required | AdminBoatDeleteView |
| /admin/clientes/ | admin_panel:clients_list | GET | admin_required | AdminClientsListView |
| /admin/clientes/<int:id>/eliminar/ | admin_panel:client_delete | POST | admin_required | AdminClientDeleteView |
| /admin/reservas/ | admin_panel:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin/reservas/<int:id>/ | admin_panel:reservation_detail | GET | admin_required | AdminReservationDetailView |
| /admin/reservas/<int:id>/cambiar-estado/ | admin_panel:change_reservation_status | POST | admin_required | AdminChangeReservationStatusView |
