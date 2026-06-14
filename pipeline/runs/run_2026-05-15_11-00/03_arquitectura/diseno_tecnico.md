---
run_id: run_2026-05-15_11-00
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-15T11:06:20+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-15_11-00`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale español.
- Backend de correo configurable (console para desarrollo, SMTP para producción).
- Datos seed idempotentes cargados en inicialización.
- Docker para empaquetado y despliegue.
- CSRF y validación de formularios Django para seguridad.

## Apps Django

### accounts

**Propósito**: Gestionar autenticación de usuarios, registro, login, logout y perfil de cliente.

**Archivos principales**

- accounts/models.py
- accounts/forms.py
- accounts/views.py
- accounts/urls.py
- templates/accounts/register.html
- templates/accounts/login.html
- templates/accounts/profile.html

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

**Propósito**: Gestionar cesta de compra, persistencia en sesión y visualización desde cualquier página.

**Archivos principales**

- cart/models.py
- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/view.html

### reservations

**Propósito**: Gestionar reservas en tres pasos, cálculo de tasa de combustible, estados, seguimiento por código y confirmación por correo.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/paypal.py
- reservations/services/email.py
- reservations/management/commands/send_payment_reminders.py
- templates/reservations/step1.html
- templates/reservations/step2.html
- templates/reservations/step3.html
- templates/reservations/confirmation.html
- templates/reservations/track.html

### admin_panel

**Propósito**: Panel de administración para gestión de barcos, clientes y reservas con cambio de estados y operaciones CRUD.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/boats_list.html
- templates/admin_panel/boat_form.html
- templates/admin_panel/clients_list.html
- templates/admin_panel/reservations_list.html
- templates/admin_panel/reservation_detail.html

### core

**Propósito**: Configuración central, utilidades, datos seed y comandos de gestión.

**Archivos principales**

- core/settings.py
- core/urls.py
- core/management/commands/seed_data.py
- core/utils.py
- templates/base.html
- templates/home.html

## Modelos

### Categoria

- **App**: catalog

**Campos**

- nombre: CharField(max_length=50, unique=True)
- descripcion: TextField(blank=True)

### Puerto

- **App**: catalog

**Campos**

- nombre: CharField(max_length=100, unique=True)
- ubicacion: CharField(max_length=200, blank=True)

### Fabricante

- **App**: catalog

**Campos**

- nombre: CharField(max_length=100, unique=True)
- pais: CharField(max_length=100, blank=True)

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
- nombre_cliente: CharField(max_length=120)
- email_cliente: EmailField()
- telefono_cliente: CharField(max_length=20, blank=True)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField(default=1)
- fecha_inicio: DateField()
- fecha_fin: DateField()
- precio_dia: DecimalField(max_digits=8, decimal_places=2)
- tasa_combustible_dia: DecimalField(max_digits=8, decimal_places=2)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- metodo_pago: CharField(choices=paypal/contra_reembolso)
- referencia_paypal: CharField(max_length=255, blank=True, null=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### HistorialEstadoReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- estado_anterior: CharField(max_length=50)
- estado_nuevo: CharField(max_length=50)
- usuario: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- fecha_cambio: DateTimeField(auto_now_add=True)
- notas: TextField(blank=True)

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
| /cesta/eliminar/ | cart:remove | POST | public | RemoveFromCartView |
| /cesta/vaciar/ | cart:clear | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:step1 | GET\|POST | public | ReservationStep1View |
| /reserva/paso2/ | reservations:step2 | GET\|POST | public | ReservationStep2View |
| /reserva/paso3/ | reservations:step3 | GET\|POST | public | ReservationStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ReservationConfirmationView |
| /reserva/seguimiento/ | reservations:track | GET\|POST | public | TrackReservationView |
| /reserva/seguimiento/<str:codigo>/ | reservations:track_detail | GET | public | TrackReservationDetailView |
| /reserva/cancelar/<str:codigo>/ | reservations:cancel | POST | public | CancelReservationView |
| /mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /mis-reservas/<int:id>/ | reservations:my_reservation_detail | GET | login_required | MyReservationDetailView |
| /paypal/return/ | reservations:paypal_return | GET | public | PayPalReturnView |
| /paypal/cancel/ | reservations:paypal_cancel | GET | public | PayPalCancelView |
| /admin/ | admin_panel:dashboard | GET | admin_required | AdminDashboardView |
| /admin/barcos/ | admin_panel:boats_list | GET | admin_required | AdminBoatsListView |
| /admin/barcos/crear/ | admin_panel:boat_create | GET\|POST | admin_required | AdminBoatCreateView |
| /admin/barcos/<int:id>/editar/ | admin_panel:boat_edit | GET\|POST | admin_required | AdminBoatEditView |
| /admin/barcos/<int:id>/eliminar/ | admin_panel:boat_delete | POST | admin_required | AdminBoatDeleteView |
| /admin/barcos/<int:id>/ | admin_panel:boat_detail | GET | admin_required | AdminBoatDetailView |
| /admin/clientes/ | admin_panel:clients_list | GET | admin_required | AdminClientsListView |
| /admin/clientes/<int:id>/ | admin_panel:client_detail | GET | admin_required | AdminClientDetailView |
| /admin/clientes/<int:id>/eliminar/ | admin_panel:client_delete | POST | admin_required | AdminClientDeleteView |
| /admin/reservas/ | admin_panel:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin/reservas/<int:id>/ | admin_panel:reservation_detail | GET | admin_required | AdminReservationDetailView |
| /admin/reservas/<int:id>/cambiar-estado/ | admin_panel:change_reservation_state | POST | admin_required | AdminChangeReservationStateView |
