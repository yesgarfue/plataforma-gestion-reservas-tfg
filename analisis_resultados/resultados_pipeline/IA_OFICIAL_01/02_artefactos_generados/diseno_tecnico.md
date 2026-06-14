---
run_id: run_2026-05-18_15-09
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-18T15:47:30+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-18_15-09`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale español configurados.
- Backend de correo Django para confirmaciones y recordatorios.
- Datos seed idempotentes precargados en cada arranque.
- Docker para empaquetado y entrega de la aplicación.
- CSRF protection y validación de formularios activos.

## Apps Django

### accounts

**Propósito**: Gestionar autenticación de usuarios: registro, login, logout y perfil de cliente.

**Archivos principales**

- accounts/models.py
- accounts/forms.py
- accounts/views.py
- accounts/urls.py
- templates/accounts/register.html
- templates/accounts/login.html
- templates/accounts/profile.html

### catalog

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda y filtros combinables.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/filters.py
- templates/catalog/list.html
- templates/catalog/detail.html

### reservations

**Propósito**: Gestionar cesta, proceso de reserva en tres pasos, pagos, estados de reserva y seguimiento por código.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/paypal.py
- reservations/services/email.py
- templates/reservations/cart.html
- templates/reservations/step1.html
- templates/reservations/step2.html
- templates/reservations/step3.html
- templates/reservations/confirmation.html

### tracking

**Propósito**: Permitir consulta de reservas por código de seguimiento sin autenticación y visualización de reservas para clientes autenticados.

**Archivos principales**

- tracking/views.py
- tracking/urls.py
- templates/tracking/search.html
- templates/tracking/detail.html
- templates/tracking/my_reservations.html

### admin_panel

**Propósito**: Proporcionar panel administrativo para gestión de barcos, clientes y reservas con cambio de estados.

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

**Propósito**: Configuración central, utilidades, comandos de gestión y datos seed.

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

- nombre: CharField(max_length=120, unique=True)
- descripcion: TextField(blank=True)

### Puerto

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120, unique=True)
- ubicacion: CharField(max_length=200, blank=True)

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
- descripcion: TextField(blank=True)
- disponible: BooleanField(default=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### LineaCarrito

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
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- nombre_cliente: CharField(max_length=120)
- email_contacto: EmailField()
- telefono: CharField(max_length=20, blank=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- fecha_inicio: DateField()
- fecha_fin: DateField()
- barcos: ManyToManyField(Barco, through=LineaReserva)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)
- tasa_combustible_dia: DecimalField(max_digits=8, decimal_places=2)

### PagoPayPal

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- transaction_id: CharField(max_length=255, unique=True, blank=True, null=True)
- estado: CharField(choices=PENDIENTE/COMPLETADO/FALLIDO, default=PENDIENTE)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | home | GET | public | HomeView |
| /accounts/registro/ | accounts:register | GET\|POST | public | RegisterView |
| /accounts/login/ | accounts:login | GET\|POST | public | LoginView |
| /accounts/logout/ | accounts:logout | GET | login_required | LogoutView |
| /accounts/perfil/ | accounts:profile | GET | login_required | ProfileView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /cesta/ | reservations:cart | GET | public | CartView |
| /cesta/agregar/ | reservations:add_to_cart | POST | public | AddToCartView |
| /cesta/actualizar/ | reservations:update_cart | POST | public | UpdateCartView |
| /cesta/vaciar/ | reservations:clear_cart | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:step1 | GET\|POST | public | ReservationStep1View |
| /reserva/paso2/ | reservations:step2 | GET\|POST | public | ReservationStep2View |
| /reserva/paso3/ | reservations:step3 | GET\|POST | public | ReservationStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ConfirmationView |
| /reserva/cancelar/<str:codigo>/ | reservations:cancel | POST | public | CancelReservationView |
| /seguimiento/ | tracking:search | GET\|POST | public | TrackingSearchView |
| /seguimiento/<str:codigo>/ | tracking:detail | GET | public | TrackingDetailView |
| /mis-reservas/ | tracking:my_reservations | GET | login_required | MyReservationsView |
| /admin-panel/ | admin_panel:dashboard | GET | admin_required | AdminDashboardView |
| /admin-panel/barcos/ | admin_panel:boats_list | GET | admin_required | AdminBoatsListView |
| /admin-panel/barcos/crear/ | admin_panel:boat_create | GET\|POST | admin_required | AdminBoatCreateView |
| /admin-panel/barcos/<int:id>/editar/ | admin_panel:boat_edit | GET\|POST | admin_required | AdminBoatEditView |
| /admin-panel/barcos/<int:id>/eliminar/ | admin_panel:boat_delete | POST | admin_required | AdminBoatDeleteView |
| /admin-panel/clientes/ | admin_panel:clients_list | GET | admin_required | AdminClientsListView |
| /admin-panel/clientes/<int:id>/eliminar/ | admin_panel:client_delete | POST | admin_required | AdminClientDeleteView |
| /admin-panel/reservas/ | admin_panel:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin-panel/reservas/<int:id>/ | admin_panel:reservation_detail | GET | admin_required | AdminReservationDetailView |
| /admin-panel/reservas/<int:id>/cambiar-estado/ | admin_panel:change_reservation_status | POST | admin_required | AdminChangeReservationStatusView |
