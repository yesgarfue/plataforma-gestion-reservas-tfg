---
run_id: run_2026-05-12_16-48
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T17:02:51+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-12_16-48`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pago online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz en español.
- Zona horaria Europe/Madrid y locale español.
- Backend de correo configurable (console para desarrollo, SMTP para producción).
- Datos seed precargados e idempotentes.
- Contenedor Docker con instrucciones en README.
- CSRF activo y contraseñas hasheadas con Django auth.

## Apps Django

### catalog

**Propósito**: Gestionar catálogo de barcos, categorías, puertos, fabricantes, búsqueda, filtros combinables y fichas detalladas de barcos.

**Archivos principales**

- catalog/models.py
- catalog/views.py
- catalog/forms.py
- catalog/urls.py
- catalog/filters.py
- templates/catalog/list.html
- templates/catalog/detail.html

### reservations

**Propósito**: Gestionar cesta, proceso de reserva en tres pasos, pagos (PayPal y contra-reembolso), estados de reserva, seguimiento por código y confirmaciones por correo.

**Archivos principales**

- reservations/models.py
- reservations/forms.py
- reservations/views.py
- reservations/urls.py
- reservations/services/paypal.py
- reservations/services/email.py
- reservations/services/pricing.py
- templates/reservations/cart.html
- templates/reservations/checkout_step1.html
- templates/reservations/checkout_step2.html
- templates/reservations/checkout_step3.html
- templates/reservations/confirmation.html

### accounts

**Propósito**: Gestionar registro, autenticación, cierre de sesión y perfil de cliente registrado.

**Archivos principales**

- accounts/models.py
- accounts/forms.py
- accounts/views.py
- accounts/urls.py
- templates/accounts/register.html
- templates/accounts/login.html
- templates/accounts/profile.html

### admin_panel

**Propósito**: Proporcionar panel de administración propio para gestionar barcos, clientes y reservas, diferente del admin de Django por defecto.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- admin_panel/decorators.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/boats_list.html
- templates/admin_panel/boats_form.html
- templates/admin_panel/clients_list.html
- templates/admin_panel/reservations_list.html
- templates/admin_panel/reservation_detail.html

### core

**Propósito**: Configuración central, utilidades, management commands para datos seed, tareas periódicas de recordatorios y middleware.

**Archivos principales**

- core/management/commands/seed_data.py
- core/tasks.py
- core/middleware.py
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
- imagen: ImageField(upload_to=barcos/)
- disponible: BooleanField(default=True)
- descripcion: TextField(blank=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- fecha_inicio: DateField
- fecha_fin: DateField
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)
- tasa_combustible_dia: DecimalField(max_digits=8, decimal_places=2)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- nombre_cliente: CharField(max_length=120)
- email_cliente: EmailField
- telefono_cliente: CharField(max_length=20, blank=True)
- lineas: ManyToManyField(LineaReserva)
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- referencia_paypal: CharField(max_length=255, blank=True, null=True)
- recordatorio_enviado: BooleanField(default=False)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

### Cesta

- **App**: reservations

**Campos**

- sesion_id: CharField(max_length=255)
- usuario: ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
- items: JSONField(default=dict)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | core:home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /registro/ | accounts:register | GET\|POST | public | RegisterView |
| /login/ | accounts:login | GET\|POST | public | LoginView |
| /logout/ | accounts:logout | POST | login_required | LogoutView |
| /perfil/ | accounts:profile | GET | login_required | ProfileView |
| /cesta/ | reservations:cart | GET | public | CartView |
| /cesta/agregar/ | reservations:add_to_cart | POST | public | AddToCartView |
| /cesta/actualizar/ | reservations:update_cart | POST | public | UpdateCartView |
| /cesta/vaciar/ | reservations:clear_cart | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:checkout_step1 | GET\|POST | public | CheckoutStep1View |
| /reserva/paso2/ | reservations:checkout_step2 | GET\|POST | public | CheckoutStep2View |
| /reserva/paso3/ | reservations:checkout_step3 | GET\|POST | public | CheckoutStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ConfirmationView |
| /reserva/paypal/return/ | reservations:paypal_return | GET | public | PayPalReturnView |
| /reserva/paypal/cancel/ | reservations:paypal_cancel | GET | public | PayPalCancelView |
| /seguimiento/ | reservations:tracking | GET\|POST | public | TrackingView |
| /mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /admin/ | admin_panel:dashboard | GET | admin_required | AdminDashboardView |
| /admin/barcos/ | admin_panel:boats_list | GET | admin_required | AdminBoatsListView |
| /admin/barcos/crear/ | admin_panel:boats_create | GET\|POST | admin_required | AdminBoatsCreateView |
| /admin/barcos/<int:id>/editar/ | admin_panel:boats_edit | GET\|POST | admin_required | AdminBoatsEditView |
| /admin/barcos/<int:id>/eliminar/ | admin_panel:boats_delete | POST | admin_required | AdminBoatsDeleteView |
| /admin/clientes/ | admin_panel:clients_list | GET | admin_required | AdminClientsListView |
| /admin/clientes/<int:id>/eliminar/ | admin_panel:clients_delete | POST | admin_required | AdminClientsDeleteView |
| /admin/reservas/ | admin_panel:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin/reservas/<int:id>/ | admin_panel:reservation_detail | GET | admin_required | AdminReservationDetailView |
| /admin/reservas/<int:id>/cambiar-estado/ | admin_panel:change_reservation_status | POST | admin_required | AdminChangeReservationStatusView |
