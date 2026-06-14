---
run_id: run_2026-05-19_02-15
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-19T02:44:08+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-19_02-15`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale español configurados.
- Backend de correo configurable para confirmaciones y recordatorios.
- Datos seed idempotentes para inicialización de catálogo y usuarios de prueba.
- Docker para empaquetado y despliegue.

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

### catalog

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda, filtros y ficha de barco.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/filters.py
- templates/catalog/list.html
- templates/catalog/detail.html

### cart

**Propósito**: Gestionar cesta de compra con persistencia en sesión, visualización y modificación de cantidades.

**Archivos principales**

- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/view.html

### reservations

**Propósito**: Gestionar reservas en tres pasos, cálculo de precios, estados, seguimiento por código y cancelación.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/pricing.py
- reservations/services/tracking.py
- templates/reservations/step1.html
- templates/reservations/step2.html
- templates/reservations/step3.html
- templates/reservations/confirmation.html

### payments

**Propósito**: Gestionar métodos de pago: PayPal Sandbox e integración, contra-reembolso y confirmación de transacciones.

**Archivos principales**

- payments/models.py
- payments/views.py
- payments/urls.py
- payments/services/paypal.py
- payments/services/cash_on_delivery.py
- templates/payments/paypal_redirect.html
- templates/payments/cash_on_delivery.html

### admin_panel

**Propósito**: Panel de administración propio para gestión de barcos, clientes, reservas y cambios de estado.

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

**Propósito**: Configuración central, utilidades, comandos de gestión y datos seed.

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
- imagen: ImageField(upload_to=barcos/, blank=True, null=True)
- disponibilidad: PositiveIntegerField(default=1)
- activo: BooleanField(default=True)
- fecha_creacion: DateTimeField(auto_now_add=True)
- fecha_actualizacion: DateTimeField(auto_now=True)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- email_contacto: EmailField()
- nombre_cliente: CharField(max_length=120)
- apellido_cliente: CharField(max_length=120)
- telefono_cliente: CharField(max_length=20, blank=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- fecha_inicio: DateField()
- fecha_fin: DateField()
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- fecha_creacion: DateTimeField(auto_now_add=True)
- fecha_actualizacion: DateTimeField(auto_now=True)
- recordatorio_enviado: BooleanField(default=False)

### LineaReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE, related_name=lineas)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField()
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)
- tasa_combustible_dia: DecimalField(max_digits=8, decimal_places=2)
- subtotal: DecimalField(max_digits=10, decimal_places=2)

### PagoPayPal

- **App**: payments

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- transaction_id: CharField(max_length=255, blank=True)
- estado: CharField(choices=PENDIENTE/COMPLETADO/FALLIDO, default=PENDIENTE)
- fecha_creacion: DateTimeField(auto_now_add=True)
- fecha_actualizacion: DateTimeField(auto_now=True)

### PagoContraReembolso

- **App**: payments

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- estado: CharField(choices=PENDIENTE/PAGADO, default=PENDIENTE)
- fecha_creacion: DateTimeField(auto_now_add=True)
- fecha_actualizacion: DateTimeField(auto_now=True)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /accounts/registro/ | accounts:register | GET\|POST | public | RegisterView |
| /accounts/login/ | accounts:login | GET\|POST | public | LoginView |
| /accounts/logout/ | accounts:logout | POST | login_required | LogoutView |
| /accounts/perfil/ | accounts:profile | GET | login_required | ProfileView |
| /cesta/ | cart:view | GET | public | CartView |
| /cesta/agregar/ | cart:add | POST | public | AddToCartView |
| /cesta/actualizar/ | cart:update | POST | public | UpdateCartView |
| /cesta/vaciar/ | cart:clear | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:step1 | GET\|POST | public | ReservationStep1View |
| /reserva/paso2/ | reservations:step2 | GET\|POST | public | ReservationStep2View |
| /reserva/paso3/ | reservations:step3 | GET\|POST | public | ReservationStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ReservationConfirmationView |
| /reserva/cancelar/<str:codigo>/ | reservations:cancel | POST | public | CancelReservationView |
| /seguimiento/ | reservations:tracking | GET\|POST | public | TrackingView |
| /seguimiento/<str:codigo>/ | reservations:tracking_detail | GET | public | TrackingDetailView |
| /mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /pago/paypal/ | payments:paypal_redirect | GET\|POST | public | PayPalRedirectView |
| /pago/paypal/return/ | payments:paypal_return | GET | public | PayPalReturnView |
| /pago/paypal/cancel/ | payments:paypal_cancel | GET | public | PayPalCancelView |
| /pago/contra-reembolso/ | payments:cash_on_delivery | GET\|POST | public | CashOnDeliveryView |
| /admin-panel/ | admin:dashboard | GET | admin_required | AdminDashboardView |
| /admin-panel/barcos/ | admin:boats_list | GET | admin_required | AdminBoatsListView |
| /admin-panel/barcos/crear/ | admin:boat_create | GET\|POST | admin_required | AdminBoatCreateView |
| /admin-panel/barcos/<int:id>/editar/ | admin:boat_edit | GET\|POST | admin_required | AdminBoatEditView |
| /admin-panel/barcos/<int:id>/eliminar/ | admin:boat_delete | POST | admin_required | AdminBoatDeleteView |
| /admin-panel/clientes/ | admin:clients_list | GET | admin_required | AdminClientsListView |
| /admin-panel/clientes/<int:id>/eliminar/ | admin:client_delete | POST | admin_required | AdminClientDeleteView |
| /admin-panel/reservas/ | admin:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin-panel/reservas/<int:id>/ | admin:reservation_detail | GET | admin_required | AdminReservationDetailView |
| /admin-panel/reservas/<int:id>/cambiar-estado/ | admin:reservation_change_state | POST | admin_required | AdminReservationChangeStateView |
