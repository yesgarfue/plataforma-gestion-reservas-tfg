---
run_id: run_2026-05-14_11-32
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T11:52:08+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-14_11-32`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale español.
- Backend de correo configurable para confirmaciones y recordatorios.
- Datos seed idempotentes precargados en Docker.
- Contenedor Docker con Dockerfile para despliegue.

## Apps Django

### accounts

**Propósito**: Gestionar autenticación, registro, login, logout y perfil de usuario cliente.

**Archivos principales**

- accounts/models.py
- accounts/views.py
- accounts/forms.py
- accounts/urls.py
- templates/accounts/register.html
- templates/accounts/login.html

### catalog

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda, filtros y ficha de barco.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/forms.py
- templates/catalog/list.html
- templates/catalog/detail.html

### cart

**Propósito**: Gestionar cesta de compra, persistencia en sesión y visualización desde cualquier página.

**Archivos principales**

- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/summary.html

### reservations

**Propósito**: Gestionar proceso de reserva en tres pasos, cálculo de importe, estados, seguimiento por código y cancelación.

**Archivos principales**

- reservations/models.py
- reservations/views.py
- reservations/forms.py
- reservations/urls.py
- reservations/services/pricing.py
- reservations/services/email.py
- templates/reservations/step1.html
- templates/reservations/step2.html
- templates/reservations/step3.html
- templates/reservations/confirmation.html

### payments

**Propósito**: Gestionar métodos de pago: PayPal Sandbox y contra-reembolso.

**Archivos principales**

- payments/views.py
- payments/urls.py
- payments/services/paypal.py
- payments/services/cash_on_delivery.py

### tracking

**Propósito**: Permitir consulta de estado de reserva por código de seguimiento sin autenticación.

**Archivos principales**

- tracking/views.py
- tracking/urls.py
- templates/tracking/search.html
- templates/tracking/detail.html

### admin_panel

**Propósito**: Panel de administración para gestión de barcos, clientes y reservas con cambio de estados.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/boats.html
- templates/admin_panel/clients.html
- templates/admin_panel/reservations.html

### core

**Propósito**: Configuración central, utilidades, comandos de seed data y tareas periódicas.

**Archivos principales**

- core/management/commands/seed_data.py
- core/tasks.py
- core/settings.py

## Modelos

### Categoria

- **App**: catalog

**Campos**

- nombre:CharField(max_length=120)
- descripcion:TextField(blank=True)

### Puerto

- **App**: catalog

**Campos**

- nombre:CharField(max_length=120)
- ubicacion:CharField(max_length=255)

### Fabricante

- **App**: catalog

**Campos**

- nombre:CharField(max_length=120)
- pais:CharField(max_length=120)

### Barco

- **App**: catalog

**Campos**

- nombre:CharField(max_length=120)
- categoria:ForeignKey(Categoria, on_delete=PROTECT)
- puerto:ForeignKey(Puerto, on_delete=PROTECT)
- fabricante:ForeignKey(Fabricante, on_delete=PROTECT)
- precio_dia:DecimalField(max_digits=8, decimal_places=2)
- capacidad:PositiveIntegerField
- imagen:ImageField(upload_to=barcos/, blank=True)
- descripcion:TextField(blank=True)
- disponible:BooleanField(default=True)
- cantidad_disponible:PositiveIntegerField(default=1)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento:CharField(max_length=32, unique=True)
- cliente:ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- email_contacto:EmailField
- nombre_cliente:CharField(max_length=120)
- apellido_cliente:CharField(max_length=120)
- telefono:CharField(max_length=20)
- fecha_inicio:DateField
- fecha_fin:DateField
- estado:CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- metodo_pago:CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- importe_total:DecimalField(max_digits=10, decimal_places=2)
- tasa_combustible:DecimalField(max_digits=8, decimal_places=2)
- fecha_creacion:DateTimeField(auto_now_add=True)
- fecha_actualizacion:DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- reserva:ForeignKey(Reserva, on_delete=CASCADE, related_name=lineas)
- barco:ForeignKey(Barco, on_delete=PROTECT)
- cantidad:PositiveIntegerField
- precio_unitario_dia:DecimalField(max_digits=8, decimal_places=2)

### TransicionEstado

- **App**: reservations

**Campos**

- reserva:ForeignKey(Reserva, on_delete=CASCADE, related_name=transiciones)
- estado_anterior:CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO)
- estado_nuevo:CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO)
- usuario:ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- fecha:DateTimeField(auto_now_add=True)
- razon:TextField(blank=True)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /cesta/ | cart:view | GET | public | CartView |
| /cesta/agregar/ | cart:add | POST | public | AddToCartView |
| /cesta/actualizar/ | cart:update | POST | public | UpdateCartView |
| /cesta/vaciar/ | cart:clear | POST | public | ClearCartView |
| /accounts/registro/ | accounts:register | GET\|POST | public | RegisterView |
| /accounts/login/ | accounts:login | GET\|POST | public | LoginView |
| /accounts/logout/ | accounts:logout | POST | login_required | LogoutView |
| /accounts/perfil/ | accounts:profile | GET | login_required | ProfileView |
| /reserva/paso1/ | reservations:step1 | GET\|POST | public | ReservationStep1View |
| /reserva/paso2/ | reservations:step2 | GET\|POST | public | ReservationStep2View |
| /reserva/paso3/ | reservations:step3 | GET\|POST | public | ReservationStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ReservationConfirmationView |
| /pago/paypal/ | payments:paypal_redirect | GET\|POST | public | PayPalRedirectView |
| /pago/paypal/return/ | payments:paypal_return | GET | public | PayPalReturnView |
| /pago/paypal/cancel/ | payments:paypal_cancel | GET | public | PayPalCancelView |
| /seguimiento/ | tracking:search | GET\|POST | public | TrackingSearchView |
| /seguimiento/<str:codigo>/ | tracking:detail | GET | public | TrackingDetailView |
| /mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /reserva/<int:id>/cancelar/ | reservations:cancel | POST | login_required | CancelReservationView |
| /admin/ | admin_panel:dashboard | GET | admin_required | AdminDashboardView |
| /admin/barcos/ | admin_panel:boats_list | GET | admin_required | AdminBoatsListView |
| /admin/barcos/crear/ | admin_panel:boat_create | GET\|POST | admin_required | AdminBoatCreateView |
| /admin/barcos/<int:id>/editar/ | admin_panel:boat_edit | GET\|POST | admin_required | AdminBoatEditView |
| /admin/barcos/<int:id>/eliminar/ | admin_panel:boat_delete | POST | admin_required | AdminBoatDeleteView |
| /admin/clientes/ | admin_panel:clients_list | GET | admin_required | AdminClientsListView |
| /admin/clientes/<int:id>/eliminar/ | admin_panel:client_delete | POST | admin_required | AdminClientDeleteView |
| /admin/reservas/ | admin_panel:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin/reservas/<int:id>/ | admin_panel:reservation_detail | GET | admin_required | AdminReservationDetailView |
| /admin/reservas/<int:id>/cambiar-estado/ | admin_panel:change_reservation_state | POST | admin_required | AdminChangeReservationStateView |
