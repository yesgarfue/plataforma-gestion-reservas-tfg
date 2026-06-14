---
run_id: run_2026-05-14_16-53
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T17:08:51+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-14_16-53`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz completamente en español.
- Zona horaria Europe/Madrid y locale español configurados.
- Backend de correo configurable (console para desarrollo, SMTP para producción).
- Datos seed idempotentes precargados en Docker.
- Autenticación estándar de Django con CSRF activo.
- Transacciones explícitas para operaciones críticas de reserva.

## Apps Django

### accounts

**Propósito**: Gestionar autenticación, registro, login, logout y cuenta de cliente. Incluye herencia de datos de sesión durante el proceso de reserva.

**Archivos principales**

- accounts/models.py
- accounts/forms.py
- accounts/views.py
- accounts/urls.py
- templates/accounts/register.html
- templates/accounts/login.html
- templates/accounts/account.html

### catalog

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda, filtros combinables y ficha de barco con selección de cantidad.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/filters.py
- templates/catalog/list.html
- templates/catalog/detail.html

### reservations

**Propósito**: Gestionar cesta, proceso de reserva en tres pasos, cálculo de tasa de combustible, métodos de pago, confirmación por correo, código de seguimiento, estados de reserva y cancelación.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/paypal.py
- reservations/services/email.py
- reservations/services/pricing.py
- templates/reservations/cart.html
- templates/reservations/step1.html
- templates/reservations/step2.html
- templates/reservations/step3.html
- templates/reservations/confirmation.html

### tracking

**Propósito**: Gestionar consulta de reservas por código de seguimiento sin autenticación y consulta de reservas del cliente autenticado.

**Archivos principales**

- tracking/views.py
- tracking/urls.py
- templates/tracking/search.html
- templates/tracking/detail.html

### admin_panel

**Propósito**: Gestionar panel de administración para barcos, clientes, reservas y transiciones de estado. Incluye alta, edición, baja de barcos y eliminación de clientes con restricción de reservas pendientes.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/boats.html
- templates/admin_panel/boat_form.html
- templates/admin_panel/clients.html
- templates/admin_panel/reservations.html

### core

**Propósito**: Configuración central, utilidades, management commands para carga de datos seed, y middleware de gestión de cesta y rol de administrador.

**Archivos principales**

- core/settings.py
- core/urls.py
- core/middleware.py
- core/management/commands/seed_data.py
- core/fixtures/seed_data.json

## Modelos

### Categoria

- **App**: catalog

**Campos**

- nombre:CharField(max_length=120, unique=True)
- descripcion:TextField(blank=True)

### Puerto

- **App**: catalog

**Campos**

- nombre:CharField(max_length=120, unique=True)
- ubicacion:CharField(max_length=255, blank=True)

### Fabricante

- **App**: catalog

**Campos**

- nombre:CharField(max_length=120, unique=True)
- pais:CharField(max_length=120, blank=True)

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
- cantidad_disponible:PositiveIntegerField(default=1)
- activo:BooleanField(default=True)
- created_at:DateTimeField(auto_now_add=True)
- updated_at:DateTimeField(auto_now=True)

### Cesta

- **App**: reservations

**Campos**

- usuario:ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
- session_key:CharField(max_length=40, blank=True)
- created_at:DateTimeField(auto_now_add=True)
- updated_at:DateTimeField(auto_now=True)

### ItemCesta

- **App**: reservations

**Campos**

- cesta:ForeignKey(Cesta, on_delete=CASCADE)
- barco:ForeignKey(Barco, on_delete=CASCADE)
- cantidad:PositiveIntegerField(default=1)
- fecha_inicio:DateField()
- fecha_fin:DateField()

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento:CharField(max_length=32, unique=True)
- cliente:ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- nombre_cliente:CharField(max_length=120)
- email_cliente:EmailField()
- telefono_cliente:CharField(max_length=20, blank=True)
- estado:CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- metodo_pago:CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- importe_total:DecimalField(max_digits=10, decimal_places=2)
- importe_combustible:DecimalField(max_digits=10, decimal_places=2)
- fecha_creacion:DateTimeField(auto_now_add=True)
- fecha_inicio:DateField()
- fecha_fin:DateField()
- notas:TextField(blank=True)
- paypal_transaction_id:CharField(max_length=255, blank=True)

### ItemReserva

- **App**: reservations

**Campos**

- reserva:ForeignKey(Reserva, on_delete=CASCADE)
- barco:ForeignKey(Barco, on_delete=CASCADE)
- cantidad:PositiveIntegerField()
- precio_unitario:DecimalField(max_digits=8, decimal_places=2)
- tasa_combustible_dia:DecimalField(max_digits=8, decimal_places=2)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /accounts/registro/ | accounts:register | GET\|POST | public | RegisterView |
| /accounts/login/ | accounts:login | GET\|POST | public | LoginView |
| /accounts/logout/ | accounts:logout | POST | login_required | LogoutView |
| /accounts/cuenta/ | accounts:account | GET | login_required | AccountView |
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
