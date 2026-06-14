---
run_id: run_2026-05-14_19-50
fase: 03_arquitectura
agente: Arquitecto
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T20:10:14+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 03 — Diseño técnico

**ID de ejecución**: `run_2026-05-14_19-50`

## Stack técnico

- Python con Django 3.2 como framework web monolítico.
- SQLite como base de datos del PMV.
- PayPal Sandbox para integración de pagos online.
- Contra-reembolso como método de pago alternativo.
- Templates Django server-side para interfaz completamente en español.
- Zona horaria Europe/Madrid y locale español configurados.
- Backend de correo configurable (console para desarrollo, SMTP para producción).
- Datos seed idempotentes precargados en cada arranque.
- Contenedor Docker con Dockerfile e instrucciones de construcción y arranque.
- CSRF activo y validación de formularios en todos los endpoints.
- Almacenamiento seguro de contraseñas con mecanismo estándar de Django.

## Apps Django

### accounts

**Propósito**: Gestionar autenticación de usuarios: registro, login, logout, perfil de cliente y validación de credenciales.

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
- catalog/forms.py
- templates/catalog/list.html
- templates/catalog/detail.html
- templates/catalog/admin_list.html
- templates/catalog/admin_form.html

### reservations

**Propósito**: Gestionar cesta, proceso de reserva en tres pasos, pagos, estados de reserva, seguimiento por código y cancelación.

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
- templates/reservations/track.html

### admin_panel

**Propósito**: Panel de administración para gestión de barcos, clientes y reservas con cambios de estado y eliminación de usuarios.

**Archivos principales**

- admin_panel/views.py
- admin_panel/urls.py
- admin_panel/forms.py
- templates/admin_panel/dashboard.html
- templates/admin_panel/boats.html
- templates/admin_panel/clients.html
- templates/admin_panel/reservations.html

### core

**Propósito**: Configuración central, utilidades, comandos de gestión de datos seed y middleware de sesión.

**Archivos principales**

- core/management/commands/seed_data.py
- core/middleware.py
- core/utils.py
- core/settings.py

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
- pais: CharField(max_length=100)

### Fabricante

- **App**: catalog

**Campos**

- nombre: CharField(max_length=100, unique=True)
- pais: CharField(max_length=100)

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
- cantidad_disponible: PositiveIntegerField(default=1)
- activo: BooleanField(default=True)

### Reserva

- **App**: reservations

**Campos**

- codigo_seguimiento: CharField(max_length=32, unique=True)
- cliente: ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
- nombre_cliente: CharField(max_length=120)
- email_cliente: EmailField
- telefono_cliente: CharField(max_length=20, blank=True)
- estado: CharField(choices=PENDIENTE_DE_PAGO/PAGADO/EN_USO/DEVUELTO, default=PENDIENTE_DE_PAGO)
- fecha_inicio: DateField
- fecha_fin: DateField
- importe_total: DecimalField(max_digits=10, decimal_places=2)
- tasa_combustible: DecimalField(max_digits=8, decimal_places=2)
- metodo_pago: CharField(choices=PAYPAL/CONTRA_REEMBOLSO)
- referencia_paypal: CharField(max_length=255, blank=True)
- creada_en: DateTimeField(auto_now_add=True)
- actualizada_en: DateTimeField(auto_now=True)

### LineaReserva

- **App**: reservations

**Campos**

- reserva: ForeignKey(Reserva, on_delete=CASCADE, related_name=lineas)
- barco: ForeignKey(Barco, on_delete=PROTECT)
- cantidad: PositiveIntegerField
- precio_unitario_dia: DecimalField(max_digits=8, decimal_places=2)

### Cesta

- **App**: reservations

**Campos**

- sesion_id: CharField(max_length=255, unique=True)
- usuario: ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
- creada_en: DateTimeField(auto_now_add=True)
- actualizada_en: DateTimeField(auto_now=True)

### LineaCesta

- **App**: reservations

**Campos**

- cesta: ForeignKey(Cesta, on_delete=CASCADE, related_name=lineas)
- barco: ForeignKey(Barco, on_delete=CASCADE)
- cantidad: PositiveIntegerField(default=1)

## Rutas

| Path | Name | Método | Auth | Vista |
|---|---|---|---|---|
| / | home | GET | public | HomeView |
| /barcos/ | catalog:barco_list | GET | public | BarcoListView |
| /barcos/<int:id>/ | catalog:barco_detail | GET | public | BarcoDetailView |
| /accounts/registro/ | accounts:register | GET\|POST | public | RegisterView |
| /accounts/login/ | accounts:login | GET\|POST | public | LoginView |
| /accounts/logout/ | accounts:logout | POST | login_required | LogoutView |
| /accounts/perfil/ | accounts:profile | GET | login_required | ProfileView |
| /cesta/ | reservations:cart | GET | public | CartView |
| /cesta/agregar/<int:barco_id>/ | reservations:add_to_cart | POST | public | AddToCartView |
| /cesta/actualizar/<int:linea_id>/ | reservations:update_cart | POST | public | UpdateCartView |
| /cesta/eliminar/<int:linea_id>/ | reservations:remove_from_cart | POST | public | RemoveFromCartView |
| /cesta/vaciar/ | reservations:clear_cart | POST | public | ClearCartView |
| /reserva/paso1/ | reservations:step1 | GET\|POST | public | ReservationStep1View |
| /reserva/paso2/ | reservations:step2 | GET\|POST | public | ReservationStep2View |
| /reserva/paso3/ | reservations:step3 | GET\|POST | public | ReservationStep3View |
| /reserva/confirmacion/ | reservations:confirmation | GET | public | ConfirmationView |
| /reserva/seguimiento/ | reservations:track | GET\|POST | public | TrackReservationView |
| /reserva/cancelar/<int:reserva_id>/ | reservations:cancel | POST | login_required | CancelReservationView |
| /mis-reservas/ | reservations:my_reservations | GET | login_required | MyReservationsView |
| /mis-reservas/<int:reserva_id>/ | reservations:reservation_detail | GET | login_required | ReservationDetailView |
| /pago/paypal/callback/ | reservations:paypal_callback | GET\|POST | public | PayPalCallbackView |
| /admin-panel/ | admin:dashboard | GET | admin_required | AdminDashboardView |
| /admin-panel/barcos/ | admin:boats_list | GET | admin_required | AdminBoatsListView |
| /admin-panel/barcos/crear/ | admin:boat_create | GET\|POST | admin_required | AdminBoatCreateView |
| /admin-panel/barcos/<int:barco_id>/editar/ | admin:boat_edit | GET\|POST | admin_required | AdminBoatEditView |
| /admin-panel/barcos/<int:barco_id>/eliminar/ | admin:boat_delete | POST | admin_required | AdminBoatDeleteView |
| /admin-panel/clientes/ | admin:clients_list | GET | admin_required | AdminClientsListView |
| /admin-panel/clientes/<int:usuario_id>/eliminar/ | admin:client_delete | POST | admin_required | AdminClientDeleteView |
| /admin-panel/reservas/ | admin:reservations_list | GET | admin_required | AdminReservationsListView |
| /admin-panel/reservas/<int:reserva_id>/cambiar-estado/ | admin:change_reservation_status | POST | admin_required | AdminChangeReservationStatusView |
