---
run_id: run_2026-05-15_09-52
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-15T09:59:34+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-15_09-52`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz completamente en español.
- Zona horaria Europe/Madrid y locale español configurados.
- Backend de correo configurable (console en desarrollo, SMTP en producción).
- Datos seed idempotentes cargados mediante comando Django personalizado.
- Contenedor Docker con Dockerfile para empaquetado y despliegue.
- CSRF activo y validación de formularios en todas las vistas.

## Apps Django

### accounts

**Propósito**: Gestionar autenticación, registro, login, logout y cuenta de cliente. Incluye validación de contraseñas y sesiones.

**Archivos principales**

- accounts/models.py
- accounts/forms.py
- accounts/views.py
- accounts/urls.py
- templates/accounts/register.html
- templates/accounts/login.html
- templates/accounts/account.html

### catalog

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda, filtros combinables y ficha de producto.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/filters.py
- templates/catalog/list.html
- templates/catalog/detail.html

### cart

**Propósito**: Gestionar cesta de compra en sesión, modificación de cantidades, visualización y vaciado de cesta.

**Archivos principales**

- cart/views.py
- cart/urls.py
- cart/services.py
- templates/cart/view.html

### reservations

**Propósito**: Gestionar reservas en tres pasos, cálculo de importe con tasa de combustible, estados de reserva, cancelación y seguimiento por código.

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

### tracking

**Propósito**: Permitir consulta de estado de reserva por código de seguimiento sin autenticación y listado de reservas para cliente autenticado.

**Archivos principales**

- tracking/views.py
- tracking/urls.py
- templates/tracking/search.html
- templates/tracking/detail.html

### admin_panel

**Propósito**: Panel de administración propio para gestión de barcos, clientes y reservas con cambios de estado y eliminaciones.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/boats.html
- templates/admin_panel/clients.html
- templates/admin_panel/reservations.html

### core

**Propósito**: Configuración central, utilidades, comandos de carga de datos seed y middleware compartido.

**Archivos principales**

- core/management/commands/load_seed_data.py
- core/middleware.py
- core/utils.py

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
- imagen: ImageField(upload_to=barcos/, blank=True)
- descripcion: TextField(blank=True)
- disponible: BooleanField(default=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- email_contacto: EmailField
- nombre_cliente: CharField(max_length=120)
- apellido_cliente: CharField(max_length=120)
- telefono_cliente: CharField(max_length=20, blank=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- fecha_inicio: DateField
- fecha_fin: DateField
- precio_base: DecimalField(max_digits=10, decimal_places=2)
- tasa_combustible: DecimalField(max_digits=10, decimal_places=2)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- referencia_paypal: CharField(max_length=255, blank=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE, related_name=lineas)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- precio_unitario: DecimalField(max_digits=8, decimal_places=2)

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
| /accounts/registro/ | accounts:register | GET\|POST | public | RegisterView |
| /accounts/login/ | accounts:login | GET\|POST | public | LoginView |
| /accounts/logout/ | accounts:logout | POST | login_required | LogoutView |
| /accounts/cuenta/ | accounts:account | GET | login_required | AccountView |
| /cesta/ | cart:view | GET | public | CartView |
| /cesta/agregar/ | cart:add | POST | public | AddToCartView |
| /cesta/actualizar/ | cart:update | POST | public | UpdateCartView |
| /cesta/vaciar/ | cart:clear | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:step1 | GET\|POST | public | ReservationStep1View |
| /reserva/paso2/ | reservations:step2 | GET\|POST | public | ReservationStep2View |
| /reserva/paso3/ | reservations:step3 | GET\|POST | public | ReservationStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ReservationConfirmationView |
| /reserva/cancelar/<int:id>/ | reservations:cancel | POST | login_required | CancelReservationView |
| /seguimiento/ | tracking:search | GET\|POST | public | TrackingSearchView |
| /seguimiento/<str:codigo>/ | tracking:detail | GET | public | TrackingDetailView |
| /mis-reservas/ | tracking:my_reservations | GET | login_required | MyReservationsView |
| /admin/ | admin:dashboard | GET | admin_required | AdminDashboardView |
| /admin/barcos/ | admin:boats_list | GET | admin_required | AdminBoatsListView |
| /admin/barcos/crear/ | admin:boat_create | GET\|POST | admin_required | AdminBoatCreateView |
| /admin/barcos/<int:id>/editar/ | admin:boat_edit | GET\|POST | admin_required | AdminBoatEditView |
| /admin/barcos/<int:id>/eliminar/ | admin:boat_delete | POST | admin_required | AdminBoatDeleteView |
| /admin/clientes/ | admin:clients_list | GET | admin_required | AdminClientsListView |
| /admin/clientes/<int:id>/eliminar/ | admin:client_delete | POST | admin_required | AdminClientDeleteView |
| /admin/reservas/ | admin:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin/reservas/<int:id>/cambiar-estado/ | admin:reservation_change_state | POST | admin_required | AdminReservationChangeStateView |
