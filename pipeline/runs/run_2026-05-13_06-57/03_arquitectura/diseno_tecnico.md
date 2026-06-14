---
run_id: run_2026-05-13_06-57
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-13T07:10:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-13_06-57`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz completamente en español.
- Zona horaria Europe/Madrid configurada en settings.
- Locale español para fechas, números y mensajes.
- Backend de correo configurable (console en desarrollo, SMTP en producción).
- Datos seed idempotentes cargados al arrancar.
- Docker para empaquetado y despliegue.
- Transacciones explícitas para evitar condiciones de carrera en SQLite.

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

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda y filtros combinables.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/filters.py
- templates/catalog/list.html
- templates/catalog/detail.html

### cart

**Propósito**: Gestionar cesta de compra persistente en sesión, modificación de cantidades y vaciado.

**Archivos principales**

- cart/models.py
- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/sidebar.html

### reservations

**Propósito**: Gestionar proceso de reserva en tres pasos, cálculo de costos con tasa de combustible, estados de reserva y seguimiento.

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
- templates/reservations/confirmation.html
- templates/reservations/tracking.html

### admin_panel

**Propósito**: Panel administrativo para gestión de barcos, clientes, reservas y cambio de estados.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/boats_list.html
- templates/admin_panel/boats_form.html
- templates/admin_panel/clients_list.html
- templates/admin_panel/reservations_list.html

### core

**Propósito**: Configuración central, utilidades, datos seed y comandos de inicialización.

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
- descripcion: TextField(blank=True)
- categoria: ForeignKey(Categoria, on_delete=PROTECT)
- puerto: ForeignKey(Puerto, on_delete=PROTECT)
- fabricante: ForeignKey(Fabricante, on_delete=PROTECT)
- precio_dia: DecimalField(max_digits=8, decimal_places=2)
- capacidad: PositiveIntegerField
- imagen: ImageField(upload_to=barcos, blank=True)
- activo: BooleanField(default=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- email_contacto: EmailField()
- nombre_contacto: CharField(max_length=120)
- telefono_contacto: CharField(max_length=20, blank=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- fecha_inicio: DateField()
- fecha_fin: DateField()
- importe_base: DecimalField(max_digits=10, decimal_places=2)
- tasa_combustible: DecimalField(max_digits=10, decimal_places=2)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- referencia_paypal: CharField(max_length=255, blank=True, null=True)
- recordatorio_enviado: BooleanField(default=False)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE, related_name=lineas)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)

### Cesta

- **App**: cart

**Campos**

- sesion_id: CharField(max_length=255, unique=True)
- usuario: ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### LineaCesta

- **App**: cart

**Campos**

- cesta: ForeignKey(Cesta, on_delete=CASCADE, related_name=lineas)
- barco: ForeignKey(Barco, on_delete=CASCADE)
- cantidad: PositiveIntegerField
- added_at: DateTimeField(auto_now_add=True)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /registro/ | accounts:register | GET\|POST | public | RegisterView |
| /login/ | accounts:login | GET\|POST | public | LoginView |
| /logout/ | accounts:logout | POST | login_required | LogoutView |
| /perfil/ | accounts:profile | GET | login_required | ProfileView |
| /cesta/ | cart:view | GET | public | CartView |
| /cesta/agregar/ | cart:add | POST | public | AddToCartView |
| /cesta/actualizar/ | cart:update | POST | public | UpdateCartView |
| /cesta/vaciar/ | cart:clear | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:checkout_step1 | GET\|POST | public | CheckoutStep1View |
| /reserva/paso2/ | reservations:checkout_step2 | GET\|POST | public | CheckoutStep2View |
| /reserva/paso3/ | reservations:checkout_step3 | GET\|POST | public | CheckoutStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ConfirmationView |
| /reserva/seguimiento/ | reservations:tracking | GET\|POST | public | TrackingView |
| /reserva/cancelar/<str:codigo>/ | reservations:cancel | POST | public | CancelReservationView |
| /mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /pago/paypal/callback/ | reservations:paypal_callback | GET\|POST | public | PayPalCallbackView |
| /admin/ | admin:dashboard | GET | admin_required | AdminDashboardView |
| /admin/barcos/ | admin:boats_list | GET | admin_required | AdminBoatsListView |
| /admin/barcos/crear/ | admin:boats_create | GET\|POST | admin_required | AdminBoatsCreateView |
| /admin/barcos/<int:id>/editar/ | admin:boats_edit | GET\|POST | admin_required | AdminBoatsEditView |
| /admin/barcos/<int:id>/eliminar/ | admin:boats_delete | POST | admin_required | AdminBoatsDeleteView |
| /admin/clientes/ | admin:clients_list | GET | admin_required | AdminClientsListView |
| /admin/clientes/<int:id>/eliminar/ | admin:clients_delete | POST | admin_required | AdminClientsDeleteView |
| /admin/reservas/ | admin:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin/reservas/<int:id>/cambiar-estado/ | admin:reservations_change_status | POST | admin_required | AdminReservationsChangeStatusView |
