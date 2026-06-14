---
run_id: run_2026-05-14_16-05
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T16:12:40+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-14_16-05`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale español configurados.
- Backend de correo configurable (console para desarrollo, SMTP para producción).
- Contra-reembolso como método de pago alternativo a PayPal.
- Docker para empaquetado y despliegue.
- Datos seed idempotentes: 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (incluyendo velero), usuarios de prueba.

## Apps Django

### accounts

**Propósito**: Gestionar autenticación de usuarios: registro, login, logout, perfil de cliente y validación de sesión.

**Archivos principales**

- accounts/models.py
- accounts/forms.py
- accounts/views.py
- accounts/urls.py
- templates/accounts/register.html
- templates/accounts/login.html
- templates/accounts/profile.html

### catalog

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda, filtros combinables y ficha de barco.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/filters.py
- templates/catalog/list.html
- templates/catalog/detail.html

### reservations

**Propósito**: Gestionar cesta, proceso de reserva en tres pasos, pagos (PayPal y contra-reembolso), estados de reserva, seguimiento por código y cancelaciones.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/paypal.py
- reservations/services/pricing.py
- reservations/services/email.py
- templates/reservations/cart.html
- templates/reservations/step1.html
- templates/reservations/step2.html
- templates/reservations/step3.html
- templates/reservations/confirmation.html
- templates/reservations/track.html

### admin_panel

**Propósito**: Panel de administración para gestionar barcos, clientes y reservas con cambios de estado y restricciones de eliminación.

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

**Propósito**: Configuración central, utilidades compartidas, comandos de gestión (seed data) y middleware.

**Archivos principales**

- core/management/commands/seed_data.py
- core/utils.py
- core/middleware.py

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
- descripcion: TextField(blank=True)
- imagen: ImageField(upload_to='barcos/', blank=True)
- categoria: ForeignKey(Categoria, on_delete=PROTECT)
- puerto: ForeignKey(Puerto, on_delete=PROTECT)
- fabricante: ForeignKey(Fabricante, on_delete=PROTECT)
- precio_dia: DecimalField(max_digits=8, decimal_places=2)
- capacidad: PositiveIntegerField
- disponible: BooleanField(default=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### ItemCesta

- **App**: reservations

**Campos**

- sesion_id: CharField(max_length=40)
- barco: ForeignKey(Barco, on_delete=CASCADE)
- cantidad: PositiveIntegerField(default=1)
- fecha_inicio: DateField()
- fecha_fin: DateField()
- created_at: DateTimeField(auto_now_add=True)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- nombre_cliente: CharField(max_length=120)
- email_contacto: EmailField()
- telefono: CharField(max_length=20, blank=True)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField(default=1)
- fecha_inicio: DateField()
- fecha_fin: DateField()
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- transaccion_paypal: CharField(max_length=255, blank=True, null=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### CambioEstadoReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- estado_anterior: CharField(max_length=50)
- estado_nuevo: CharField(max_length=50)
- usuario: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- timestamp: DateTimeField(auto_now_add=True)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | catalog:home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /buscar/ | catalog:search | GET | public | SearchView |
| /accounts/registro/ | accounts:register | GET\|POST | public | RegisterView |
| /accounts/login/ | accounts:login | GET\|POST | public | LoginView |
| /accounts/logout/ | accounts:logout | POST | login_required | LogoutView |
| /accounts/perfil/ | accounts:profile | GET | login_required | ProfileView |
| /cesta/ | reservations:cart | GET | public | CartView |
| /cesta/agregar/ | reservations:add_to_cart | POST | public | AddToCartView |
| /cesta/actualizar/ | reservations:update_cart | POST | public | UpdateCartView |
| /cesta/vaciar/ | reservations:clear_cart | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:step1 | GET\|POST | public | ReservationStep1View |
| /reserva/paso2/ | reservations:step2 | GET\|POST | public | ReservationStep2View |
| /reserva/paso3/ | reservations:step3 | GET\|POST | public | ReservationStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ConfirmationView |
| /reserva/seguimiento/ | reservations:track | GET\|POST | public | TrackReservationView |
| /paypal/return/ | reservations:paypal_return | GET | public | PayPalReturnView |
| /paypal/cancel/ | reservations:paypal_cancel | GET | public | PayPalCancelView |
| /mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /reserva/<int:id>/cancelar/ | reservations:cancel | POST | login_required | CancelReservationView |
| /admin-panel/ | admin:dashboard | GET | admin_required | AdminDashboardView |
| /admin-panel/barcos/ | admin:boats_list | GET | admin_required | AdminBoatsListView |
| /admin-panel/barcos/crear/ | admin:boat_create | GET\|POST | admin_required | AdminBoatCreateView |
| /admin-panel/barcos/<int:id>/editar/ | admin:boat_edit | GET\|POST | admin_required | AdminBoatEditView |
| /admin-panel/barcos/<int:id>/eliminar/ | admin:boat_delete | POST | admin_required | AdminBoatDeleteView |
| /admin-panel/clientes/ | admin:clients_list | GET | admin_required | AdminClientsListView |
| /admin-panel/clientes/<int:id>/eliminar/ | admin:client_delete | POST | admin_required | AdminClientDeleteView |
| /admin-panel/reservas/ | admin:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin-panel/reservas/<int:id>/ | admin:reservation_detail | GET | admin_required | AdminReservationDetailView |
| /admin-panel/reservas/<int:id>/cambiar-estado/ | admin:change_reservation_status | POST | admin_required | AdminChangeReservationStatusView |
