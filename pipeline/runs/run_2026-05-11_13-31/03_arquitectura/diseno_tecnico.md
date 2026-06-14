---
run_id: run_2026-05-11_13-31
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-11T14:26:34+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 1
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-11_13-31`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale español configurados.
- Backend de correo SMTP para envío de confirmaciones.
- Datos seed idempotentes para barcos, categorías, puertos y fabricantes.
- Docker para empaquetado y despliegue.

## Apps Django

### catalog

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda, filtros por disponibilidad de fechas y ficha detallada de barco.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/urls.py
- catalog/forms.py
- templates/catalog/list.html
- templates/catalog/detail.html

### reservations

**Propósito**: Gestionar cesta, proceso de reserva en tres pasos, métodos de pago (PayPal y contra-reembolso), estados de reserva, seguimiento por código y confirmación por correo.

**Archivos principales**

- reservations/models.py
- reservations/views.py
- reservations/urls.py
- reservations/forms.py
- reservations/services/paypal.py
- reservations/services/email.py
- templates/reservations/cart.html
- templates/reservations/checkout_step1.html
- templates/reservations/checkout_step2.html
- templates/reservations/checkout_step3.html
- templates/reservations/confirmation.html
- templates/reservations/tracking.html

### accounts

**Propósito**: Gestionar registro, inicio de sesión, cierre de sesión y autenticación de clientes.

**Archivos principales**

- accounts/models.py
- accounts/views.py
- accounts/urls.py
- accounts/forms.py
- templates/accounts/register.html
- templates/accounts/login.html

### admin_panel

**Propósito**: Proporcionar panel de administración para gestionar barcos, clientes, reservas y cambio de estados.

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

**Propósito**: Configuración central, utilidades, comandos de gestión y datos seed.

**Archivos principales**

- core/management/commands/seed_data.py
- core/settings.py
- core/urls.py

## Modelos

### Categoria

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120)
- descripcion: TextField(blank=True)

### Puerto

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120)
- ubicacion: CharField(max_length=200)

### Fabricante

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120)
- pais: CharField(max_length=120)

### Barco

- **App**: catalog

**Campos**

- nombre: CharField(max_length=120)
- categoria: ForeignKey(Categoria, on_delete=PROTECT)
- puerto: ForeignKey(Puerto, on_delete=PROTECT)
- fabricante: ForeignKey(Fabricante, on_delete=PROTECT)
- precio_dia: DecimalField(max_digits=8, decimal_places=2)
- capacidad: PositiveIntegerField()
- descripcion: TextField(blank=True)
- imagen: ImageField(upload_to=barcos/, blank=True)

### CartItem

- **App**: reservations

**Campos**

- barco: ForeignKey(Barco, on_delete=CASCADE)
- cantidad: PositiveIntegerField(default=1)
- fecha_inicio: DateField()
- fecha_fin: DateField()
- session_key: CharField(max_length=40)
- usuario: ForeignKey(User, null=True, blank=True, on_delete=CASCADE)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- nombre_contacto: CharField(max_length=120)
- email_contacto: EmailField()
- telefono_contacto: CharField(max_length=20)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- metodo_pago: CharField(choices=paypal/contra_reembolso)
- fecha_creacion: DateTimeField(auto_now_add=True)
- fecha_inicio: DateField()
- fecha_fin: DateField()

### ReservaItem

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField()
- precio_unitario: DecimalField(max_digits=8, decimal_places=2)
- subtotal: DecimalField(max_digits=10, decimal_places=2)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /cesta/ | reservations:cart | GET | public | CartView |
| /cesta/agregar/ | reservations:add_to_cart | POST | public | AddToCartView |
| /cesta/actualizar/ | reservations:update_cart | POST | public | UpdateCartView |
| /cesta/eliminar/ | reservations:remove_from_cart | POST | public | RemoveFromCartView |
| /reserva/paso1/ | reservations:checkout_step1 | GET\|POST | public | CheckoutStep1View |
| /reserva/paso2/ | reservations:checkout_step2 | GET\|POST | public | CheckoutStep2View |
| /reserva/paso3/ | reservations:checkout_step3 | GET\|POST | public | CheckoutStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ConfirmationView |
| /pago/paypal/callback/ | reservations:paypal_callback | GET\|POST | public | PayPalCallbackView |
| /pago/paypal/cancel/ | reservations:paypal_cancel | GET | public | PayPalCancelView |
| /seguimiento/ | reservations:tracking | GET\|POST | public | TrackingView |
| /registro/ | accounts:register | GET\|POST | public | RegisterView |
| /login/ | accounts:login | GET\|POST | public | LoginView |
| /logout/ | accounts:logout | POST | login_required | LogoutView |
| /mi-cuenta/ | accounts:profile | GET | login_required | ProfileView |
| /mis-reservas/ | accounts:my_reservations | GET | login_required | MyReservationsView |
| /reserva/<int:id>/cancelar/ | reservations:cancel_reservation | POST | login_required | CancelReservationView |
| /admin/ | admin:dashboard | GET | admin_required | AdminDashboardView |
| /admin/barcos/ | admin:boats_list | GET | admin_required | AdminBoatsListView |
| /admin/barcos/crear/ | admin:boats_create | GET\|POST | admin_required | AdminBoatsCreateView |
| /admin/barcos/<int:id>/editar/ | admin:boats_edit | GET\|POST | admin_required | AdminBoatsEditView |
| /admin/barcos/<int:id>/eliminar/ | admin:boats_delete | POST | admin_required | AdminBoatsDeleteView |
| /admin/clientes/ | admin:clients_list | GET | admin_required | AdminClientsListView |
| /admin/clientes/<int:id>/eliminar/ | admin:clients_delete | POST | admin_required | AdminClientsDeleteView |
| /admin/reservas/ | admin:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin/reservas/<int:id>/ | admin:reservations_detail | GET\|POST | admin_required | AdminReservationsDetailView |
