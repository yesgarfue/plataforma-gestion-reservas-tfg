---
run_id: run_2026-05-12_15-34
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T15:58:14+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-12_15-34`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para el flujo de pago online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para la interfaz en español.
- Zona horaria Europe/Madrid y locale español.
- Backend de correo configurable (console para desarrollo, SMTP para producción).
- Datos seed idempotentes con 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (una velero), usuario admin y usuario cliente.
- Contenedor Docker con instrucciones de construcción y arranque.
- Protección CSRF en formularios y autenticación segura con contraseñas hasheadas.

## Apps Django

### core

**Propósito**: Gestionar autenticación de usuarios, registro, login, logout, datos seed y configuración global de la aplicación.

**Archivos principales**

- core/models.py
- core/views.py
- core/forms.py
- core/urls.py
- core/management/commands/seed_data.py
- templates/core/register.html
- templates/core/login.html

### catalog

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda, filtros combinables y ficha detallada de barco.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/filters.py
- templates/catalog/list.html
- templates/catalog/detail.html

### cart

**Propósito**: Gestionar cesta de compra visible desde cualquier página, modificación de cantidades, vaciado y persistencia en sesión.

**Archivos principales**

- cart/models.py
- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/cart_widget.html

### reservations

**Propósito**: Gestionar reservas en tres pasos, pago PayPal y contra-reembolso, estados de reserva, seguimiento por código, cancelación, recordatorios por email y gestión administrativa.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/paypal.py
- reservations/services/email.py
- reservations/management/commands/send_reminders.py
- templates/reservations/checkout_step1.html
- templates/reservations/checkout_step2.html
- templates/reservations/checkout_step3.html
- templates/reservations/tracking.html
- templates/reservations/history.html

### admin_panel

**Propósito**: Gestionar reservas, clientes y barcos desde panel administrativo. Cambiar estados de reserva, eliminar clientes sin reservas pendientes.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- templates/admin_panel/reservations_list.html
- templates/admin_panel/clients_list.html
- templates/admin_panel/boats_list.html

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
- ubicacion: CharField(max_length=255)

### Fabricante

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120, unique=True)
- pais: CharField(max_length=120, blank=True)

### Barco

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120)
- descripcion: TextField()
- categoria: ForeignKey(Categoria, on_delete=PROTECT)
- puerto: ForeignKey(Puerto, on_delete=PROTECT)
- fabricante: ForeignKey(Fabricante, on_delete=PROTECT)
- precio_dia: DecimalField(max_digits=8, decimal_places=2)
- capacidad: PositiveIntegerField()
- cantidad_disponible: PositiveIntegerField()
- created_at: DateTimeField(auto_now_add=True)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- nombre_cliente: CharField(max_length=120)
- email_cliente: EmailField()
- telefono_cliente: CharField(max_length=20, blank=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- importe_combustible: DecimalField(max_digits=10, decimal_places=2)
- fecha_inicio: DateField()
- fecha_fin: DateField()
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE, related_name=lineas)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField()
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)
- subtotal: DecimalField(max_digits=10, decimal_places=2)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | core:home | GET | public | HomeView |
| /registro/ | core:register | GET\|POST | public | RegisterView |
| /login/ | core:login | GET\|POST | public | LoginView |
| /logout/ | core:logout | POST | login_required | LogoutView |
| /cuenta/ | core:account | GET | login_required | AccountView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /cesta/ | cart:cart_view | GET | public | CartView |
| /cesta/agregar/ | cart:add_to_cart | POST | public | AddToCartView |
| /cesta/actualizar/ | cart:update_cart | POST | public | UpdateCartView |
| /cesta/vaciar/ | cart:clear_cart | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:checkout_step1 | GET\|POST | public | CheckoutStep1View |
| /reserva/paso2/ | reservations:checkout_step2 | GET\|POST | public | CheckoutStep2View |
| /reserva/paso3/ | reservations:checkout_step3 | GET\|POST | public | CheckoutStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ConfirmationView |
| /reserva/paypal/return/ | reservations:paypal_return | GET | public | PayPalReturnView |
| /reserva/paypal/cancel/ | reservations:paypal_cancel | GET | public | PayPalCancelView |
| /seguimiento/ | reservations:tracking | GET\|POST | public | TrackingView |
| /mis-reservas/ | reservations:history | GET | login_required | ReservationHistoryView |
| /reserva/<int:id>/cancelar/ | reservations:cancel | POST | login_required | CancelReservationView |
| /admin/reservas/ | admin_panel:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin/reservas/<int:id>/cambiar-estado/ | admin_panel:change_reservation_status | POST | admin_required | ChangeReservationStatusView |
| /admin/clientes/ | admin_panel:clients_list | GET | admin_required | AdminClientsListView |
| /admin/clientes/<int:id>/eliminar/ | admin_panel:delete_client | POST | admin_required | DeleteClientView |
| /admin/barcos/ | admin_panel:boats_list | GET | admin_required | AdminBoatsListView |
