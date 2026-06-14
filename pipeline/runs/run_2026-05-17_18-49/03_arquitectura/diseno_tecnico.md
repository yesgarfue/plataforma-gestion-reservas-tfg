---
run_id: run_2026-05-17_18-49
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-17T19:37:59+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 1
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-17_18-49`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para flujo de pago online simulado y reproducible sin dependencia obligatoria de API externa.
- Contra-reembolso como método de pago alternativo funcional.
- Templates Django server-side para interfaz completamente en español.
- Zona horaria Europe/Madrid y locale español configurados.
- Backend de correo configurable (console backend para desarrollo, SMTP para producción).
- Datos seed idempotentes cargados mediante management command.
- Docker para empaquetado y despliegue con Dockerfile e instrucciones en README.
- CSRF activo y validación de formularios en todas las vistas.

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

### cart

**Propósito**: Gestionar cesta de compra: añadir, modificar cantidad, revisar estado y vaciar. La cesta se vacía al entrar en modo administrador.

**Archivos principales**

- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/view.html

### reservations

**Propósito**: Gestionar proceso de reserva en tres pasos, cálculo de tarifa con tasa de combustible, estados de reserva, seguimiento por código y consulta de reservas del cliente autenticado.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/pricing.py
- reservations/services/paypal.py
- reservations/services/email.py
- templates/reservations/step1.html
- templates/reservations/step2.html
- templates/reservations/step3.html
- templates/reservations/confirmation.html
- templates/reservations/tracking.html

### admin_panel

**Propósito**: Panel de administración propio para gestión de barcos, clientes y reservas. Incluye alta, edición, baja de barcos; consulta y eliminación de clientes respetando restricción de reservas pendientes; consulta y cambio de estado de reservas.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- admin_panel/services.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/boats_list.html
- templates/admin_panel/boat_form.html
- templates/admin_panel/clients_list.html
- templates/admin_panel/reservations_list.html

### core

**Propósito**: Configuración central, utilidades compartidas, comando de management para datos seed idempotentes y configuración de zona horaria y locale.

**Archivos principales**

- core/management/commands/seed_data.py
- core/settings.py
- core/utils.py

## Modelos

### Categoria

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120, unique=True)

### Puerto

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120, unique=True)

### Fabricante

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120, unique=True)

### Barco

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120)
- categoria: ForeignKey(Categoria, on_delete=PROTECT)
- puerto: ForeignKey(Puerto, on_delete=PROTECT)
- fabricante: ForeignKey(Fabricante, on_delete=PROTECT)
- precio_dia: DecimalField(max_digits=8, decimal_places=2)
- capacidad: PositiveIntegerField
- imagen: ImageField(upload_to=barcos/, null=True, blank=True)
- disponibilidad: PositiveIntegerField(default=1)
- descripcion: TextField(blank=True)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- nombre_cliente: CharField(max_length=120)
- email_contacto: EmailField
- telefono: CharField(max_length=20, blank=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- fecha_inicio: DateField
- fecha_fin: DateField
- cantidad_barcos: PositiveIntegerField
- fecha_creacion: DateTimeField(auto_now_add=True)
- fecha_actualizacion: DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)
- tasa_combustible_dia: DecimalField(max_digits=8, decimal_places=2)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /accounts/registro/ | accounts:register | GET\|POST | public | RegisterView |
| /accounts/login/ | accounts:login | GET\|POST | public | LoginView |
| /accounts/logout/ | accounts:logout | GET | login_required | LogoutView |
| /accounts/cuenta/ | accounts:account | GET | login_required | AccountView |
| /cesta/ | cart:view | GET | public | CartView |
| /cesta/anadir/ | cart:add | POST | public | AddToCartView |
| /cesta/actualizar/ | cart:update | POST | public | UpdateCartView |
| /cesta/vaciar/ | cart:clear | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:step1 | GET\|POST | public | ReservationStep1View |
| /reserva/paso2/ | reservations:step2 | GET\|POST | public | ReservationStep2View |
| /reserva/paso3/ | reservations:step3 | GET\|POST | public | ReservationStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ReservationConfirmationView |
| /seguimiento/ | reservations:tracking | GET\|POST | public | TrackingView |
| /mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /paypal/return/ | reservations:paypal_return | GET | public | PayPalReturnView |
| /paypal/cancel/ | reservations:paypal_cancel | GET | public | PayPalCancelView |
| /admin-panel/ | admin_panel:dashboard | GET | admin_required | AdminDashboardView |
| /admin-panel/barcos/ | admin_panel:boats_list | GET | admin_required | AdminBoatsListView |
| /admin-panel/barcos/crear/ | admin_panel:boat_create | GET\|POST | admin_required | AdminBoatCreateView |
| /admin-panel/barcos/<int:id>/editar/ | admin_panel:boat_edit | GET\|POST | admin_required | AdminBoatEditView |
| /admin-panel/barcos/<int:id>/eliminar/ | admin_panel:boat_delete | POST | admin_required | AdminBoatDeleteView |
| /admin-panel/clientes/ | admin_panel:clients_list | GET | admin_required | AdminClientsListView |
| /admin-panel/clientes/<int:id>/eliminar/ | admin_panel:client_delete | POST | admin_required | AdminClientDeleteView |
| /admin-panel/reservas/ | admin_panel:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin-panel/reservas/<int:id>/ | admin_panel:reservation_detail | GET | admin_required | AdminReservationDetailView |
| /admin-panel/reservas/<int:id>/cambiar-estado/ | admin_panel:reservation_change_state | POST | admin_required | AdminReservationChangeStateView |
