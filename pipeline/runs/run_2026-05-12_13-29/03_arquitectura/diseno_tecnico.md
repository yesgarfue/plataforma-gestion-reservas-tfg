---
run_id: run_2026-05-12_13-29
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T13:55:13+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-12_13-29`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale español configurados.
- Backend de correo configurable (console para desarrollo, SMTP para producción).
- Datos seed idempotentes precargados en cada arranque.
- Contenedor Docker para empaquetado y despliegue.
- Transacciones explícitas con aislamiento SERIALIZABLE para concurrencia en SQLite.
- Protección CSRF activa en todos los formularios.
- Contraseñas hasheadas con algoritmo seguro de Django.

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

**Propósito**: Gestionar cesta de compra: agregar, modificar cantidad, eliminar barcos, mantener estado entre sesiones.

**Archivos principales**

- cart/models.py
- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/view.html

### reservations

**Propósito**: Gestionar reservas en tres pasos, pagos, estados, códigos de seguimiento y consulta de estado.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/paypal.py
- reservations/services/email.py
- reservations/services/pricing.py
- templates/reservations/checkout_step1.html
- templates/reservations/checkout_step2.html
- templates/reservations/checkout_step3.html
- templates/reservations/tracking.html

### admin_panel

**Propósito**: Gestionar barcos, clientes y reservas desde panel administrativo con cambios de estado y validaciones.

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

**Propósito**: Configuración central, utilidades, comandos de seed data, middleware y settings.

**Archivos principales**

- core/settings.py
- core/urls.py
- core/middleware.py
- core/management/commands/seed_data.py
- core/utils.py

## Modelos

### Categoria

- **App**: catalog

**Campos**

- nombre: CharField(max_length=100, unique=True)
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
- imagen: ImageField(upload_to=barcos/)
- categoria: ForeignKey(Categoria, on_delete=PROTECT)
- puerto: ForeignKey(Puerto, on_delete=PROTECT)
- fabricante: ForeignKey(Fabricante, on_delete=PROTECT)
- capacidad: PositiveIntegerField
- precio_dia: DecimalField(max_digits=8, decimal_places=2)
- disponible: BooleanField(default=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### Cesta

- **App**: cart

**Campos**

- usuario: ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
- sesion_id: CharField(max_length=40, blank=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### ItemCesta

- **App**: cart

**Campos**

- cesta: ForeignKey(Cesta, on_delete=CASCADE)
- barco: ForeignKey(Barco, on_delete=CASCADE)
- cantidad: PositiveIntegerField(default=1)
- fecha_inicio: DateField()
- fecha_fin: DateField()

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
- importe_base: DecimalField(max_digits=10, decimal_places=2)
- tasa_combustible: DecimalField(max_digits=10, decimal_places=2)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- fecha_creacion: DateTimeField(auto_now_add=True)
- fecha_inicio: DateField()
- fecha_fin: DateField()
- paypal_transaction_id: CharField(max_length=100, blank=True, null=True)
- recordatorio_enviado: BooleanField(default=False)

### ItemReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)

### HistorialEstadoReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- estado_anterior: CharField(max_length=50)
- estado_nuevo: CharField(max_length=50)
- usuario_cambio: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- fecha_cambio: DateTimeField(auto_now_add=True)
- notas: TextField(blank=True)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | core:home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /buscar/ | catalog:search | GET | public | BarcoSearchView |
| /registro/ | accounts:register | GET\|POST | public | RegisterView |
| /login/ | accounts:login | GET\|POST | public | LoginView |
| /logout/ | accounts:logout | POST | login_required | LogoutView |
| /perfil/ | accounts:profile | GET | login_required | ProfileView |
| /cesta/ | cart:view | GET | public | CartView |
| /cesta/agregar/ | cart:add | POST | public | AddToCartView |
| /cesta/actualizar/ | cart:update | POST | public | UpdateCartView |
| /cesta/eliminar/<int:item_id>/ | cart:remove | POST | public | RemoveFromCartView |
| /reserva/paso1/ | reservations:checkout_step1 | GET\|POST | public | CheckoutStep1View |
| /reserva/paso2/ | reservations:checkout_step2 | GET\|POST | public | CheckoutStep2View |
| /reserva/paso3/ | reservations:checkout_step3 | GET\|POST | public | CheckoutStep3View |
| /reserva/pago-paypal/ | reservations:paypal_payment | GET\|POST | public | PayPalPaymentView |
| /reserva/paypal-callback/ | reservations:paypal_callback | GET | public | PayPalCallbackView |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ConfirmationView |
| /seguimiento/ | reservations:tracking | GET\|POST | public | TrackingView |
| /mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /reserva/<int:id>/cancelar/ | reservations:cancel | POST | login_required | CancelReservationView |
| /admin/ | admin_panel:dashboard | GET | admin_required | AdminDashboardView |
| /admin/barcos/ | admin_panel:boats_list | GET | admin_required | AdminBoatsListView |
| /admin/barcos/crear/ | admin_panel:boats_create | GET\|POST | admin_required | AdminBoatsCreateView |
| /admin/barcos/<int:id>/editar/ | admin_panel:boats_edit | GET\|POST | admin_required | AdminBoatsEditView |
| /admin/barcos/<int:id>/eliminar/ | admin_panel:boats_delete | POST | admin_required | AdminBoatsDeleteView |
| /admin/clientes/ | admin_panel:clients_list | GET | admin_required | AdminClientsListView |
| /admin/clientes/<int:id>/eliminar/ | admin_panel:clients_delete | POST | admin_required | AdminClientsDeleteView |
| /admin/reservas/ | admin_panel:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin/reservas/<int:id>/cambiar-estado/ | admin_panel:change_reservation_status | POST | admin_required | AdminChangeReservationStatusView |
