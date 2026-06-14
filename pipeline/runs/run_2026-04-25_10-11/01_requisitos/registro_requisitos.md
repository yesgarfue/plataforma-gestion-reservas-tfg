---
run_id: run_2026-04-25_10-11
fase: 01_requisitos
agente: Analista
modelo: ollama/qwen2.5-coder:7b
timestamp: 2026-04-25T10:30:52+02:00
hash_brief: sha256:e62bcd5b2a4f5684...
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-04-25_10-11`

## Requisitos funcionales

Total: **22**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El cliente puede reservar un barco sin registro previo. | Media |
| RF-05 | El cliente puede iniciar sesión durante la compra con recuperación de cesta. | Media |
| RF-06 | El administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La página principal muestra catálogo de barcos organizado por categorías. | Alta |
| RF-08 | Los filtros de puertos, fabricantes y precio se presentan como desplegables con valores válidos. | Alta |
| RF-09 | Los filtros de puerto y fabricante se pueden utilizar en combinación. | Media |
| RF-10 | El usuario puede revisar el estado de la cesta desde el catálogo. | Alta |
| RF-11 | Al entrar en modo administrador, la cesta se vacía automáticamente y el administrador no puede añadir barcos al carro. | Alta |
| RF-12 | El proceso de reserva se realiza en no más de tres pasos, sin exigir registro previo. | Alta |
| RF-13 | Los métodos de pago disponibles son PayPal Sandbox y contra-reembolso. | Alta |
| RF-14 | El cliente recibe un correo electrónico con los datos del barco reservado, el rango de fechas, el importe total y un código de seguimiento del alquiler. | Alta |
| RF-15 | Se aplica una tasa de combustible de 50 € por día, salvo que el barco sea de categoría 'velero', en cuyo caso la tasa es 0 €. | Alta |
| RF-16 | Una reserva puede cancelarse unicamente si está en estado PENDIENTE DE PAGO. | Alta |
| RF-17 | Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario. | Alta |
| RF-18 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email. | Alta |
| RF-19 | El administrador puede consultar el estado de cualquier reserva desde el panel de reservas. | Alta |
| RF-20 | El panel de administración permite gestionar barcos (alta, edición, baja). | Alta |
| RF-21 | El panel de administración permite gestionar clientes (consulta y eliminación con restricción de no eliminar usuarios con reservas pendientes). | Alta |
| RF-22 | El panel de administración permite gestionar reservas (consulta, cambio de estado). | Alta |

## Requisitos no funcionales

Total: **6**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Idioma | La interfaz de usuario está íntegramente en español. | Alta |
| RNF-02 | Framework web | La aplicación se desarrolla utilizando Django 3.2. | Alta |
| RNF-03 | Base de datos | La aplicación utiliza SQLite como base de datos. | Alta |
| RNF-04 | Seguridad | Contraseñas no almacenadas en texto plano (método estándar de Django); CSRF activo. | Alta |
| RNF-05 | Empaquetado | La aplicación debe entregarse como contenedor Docker, siguiendo las instrucciones en el README. | Alta |
| RNF-06 | Datos de ejemplo | La aplicación se debe arrancar con datos precargados (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, 1 administrador, 1 cliente). | Alta |
