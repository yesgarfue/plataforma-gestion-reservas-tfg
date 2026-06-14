---
run_id: run_2026-05-18_16-37
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-18T19:46:43+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 1
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-18_16-37`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale español.
- Backend de correo configurable (console en desarrollo, SMTP en producción).
- Datos seed idempotentes con mínimo 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (incluyendo velero), 1 admin y 1 cliente de prueba.
- Docker para empaquetado y despliegue.
- Seguridad: CSRF activo, contraseñas hasheadas con mecanismo estándar de Django, validación de formularios en servidor.

## Apps Django

### accounts

**Propósito**: Gestionar autenticación de clientes: registro, login, logout, perfil de usuario y consulta de reservas del cliente autenticado.

**Archivos principales**

- accounts/models.py
- accounts/forms.py
- accounts/views.py
- accounts/urls.py
- templates/accounts/register.html
- templates/accounts/login.html
- templates/accounts/profile.html

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

**Propósito**: Gestionar cesta de compra: almacenamiento en sesión, modificación de cantidades, visualización y vaciado al entrar en modo administrador.

**Archivos principales**

- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/view.html

### reservations

**Propósito**: Gestionar reservas en tres pasos, métodos de pago (PayPal Sandbox y contra-reembolso), cálculo de tasa de combustible, estados de reserva, cancelación, seguimiento por código y recordatorios de pago.

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

**Propósito**: Panel administrativo para gestión de barcos (alta, edición, baja), clientes (consulta, eliminación con restricción) y reservas (consulta, cambio de estado con transiciones aplicables).

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/boats_list.html
- templates/admin_panel/boats_form.html
- templates/admin_panel/clients_list.html
- templates/admin_panel/reservations_list.html
- templates/admin_panel/reservations_detail.html

### core

**Propósito**: Configuración central, datos seed, utilidades comunes y gestión de zona horaria y locale.

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
- descripcion: TextField(blank=True)
- disponible: BooleanField(default=True)
- cantidad_disponible: PositiveIntegerField(default=1)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- nombre_cliente: CharField(max_length=120)
- email_cliente: EmailField
- telefono_cliente: CharField(max_length=20, blank=True)
- fecha_inicio: DateField
- fecha_fin: DateField
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- tasa_combustible: DecimalField(max_digits=10, decimal_places=2)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE, related_name=lineas)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)

### User

- **App**: accounts

**Campos**

- email: EmailField(unique=True)
- nombre: CharField(max_length=120, blank=True)
- telefono: CharField(max_length=20, blank=True)
- es_administrador: BooleanField(default=False)
- password: CharField(max_length=255)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | core:home | GET | public | HomeView |
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
| /reserva/seguimiento/ | reservations:track | GET\|POST | public | TrackReservationView |
| /reserva/mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /reserva/<int:id>/cancelar/ | reservations:cancel | POST | public | CancelReservationView |
| /paypal/return/ | reservations:paypal_return | GET | public | PayPalReturnView |
| /paypal/cancel/ | reservations:paypal_cancel | GET | public | PayPalCancelView |
| /admin-panel/ | admin_panel:dashboard | GET | admin_required | AdminDashboardView |
| /admin-panel/barcos/ | admin_panel:boats_list | GET | admin_required | AdminBoatsListView |
| /admin-panel/barcos/crear/ | admin_panel:boats_create | GET\|POST | admin_required | AdminBoatsCreateView |
| /admin-panel/barcos/<int:id>/editar/ | admin_panel:boats_edit | GET\|POST | admin_required | AdminBoatsEditView |
| /admin-panel/barcos/<int:id>/eliminar/ | admin_panel:boats_delete | POST | admin_required | AdminBoatsDeleteView |
| /admin-panel/clientes/ | admin_panel:clients_list | GET | admin_required | AdminClientsListView |
| /admin-panel/clientes/<int:id>/eliminar/ | admin_panel:clients_delete | POST | admin_required | AdminClientsDeleteView |
| /admin-panel/reservas/ | admin_panel:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin-panel/reservas/<int:id>/ | admin_panel:reservations_detail | GET | admin_required | AdminReservationsDetailView |
| /admin-panel/reservas/<int:id>/cambiar-estado/ | admin_panel:reservations_change_state | POST | admin_required | AdminReservationsChangeStateView |
