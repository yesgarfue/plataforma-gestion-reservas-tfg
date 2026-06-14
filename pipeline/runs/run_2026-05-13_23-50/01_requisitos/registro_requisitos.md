---
run_id: run_2026-05-13_23-50
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-14T01:01:28+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 3
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-13_23-50`

## Requisitos funcionales

Total: **29**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El registro de cliente es opcional para la reserva. | Alta |
| RF-05 | El inicio de sesión puede realizarse durante el proceso de reserva, recuperando la cesta y continuando el proceso. | Baja |
| RF-06 | Un administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La página principal muestra el catálogo de barcos organizado por categorías. | Alta |
| RF-08 | Los clientes pueden buscar barcos por nombre o título. | Alta |
| RF-09 | Existen filtros combinables para puertos, fabricantes, precio, categoría y capacidad de barco. | Baja |
| RF-10 | Los barcos no disponibles en un rango de fechas aparecen marcados como 'No disponible'. | Alta |
| RF-11 | El cliente puede seleccionar la cantidad de unidades del barco y añadirlo a la cesta. | Alta |
| RF-12 | La cesta está siempre visible desde cualquier página y permite la modificación de cantidades de cada barco. | Baja |
| RF-13 | El administrador al entrar en modo administrador ve una cesta vacía y no puede añadir al carro. | Alta |
| RF-14 | El cliente puede finalizar la compra del proceso de reserva, pasándolo a tres pasos sin exigir registro previo. | Baja |
| RF-15 | La aplicación acepta dos métodos de pago: PayPal Sandbox y contra-reembolso. | Alta |
| RF-16 | El cliente recibe un correo electrónico con los datos del barco reservado, el rango de fechas, el importe total y un código de seguimiento del alquiler. | Alta |
| RF-17 | Se aplica una tasa de combustible de 50 € por día, excepto para los barcos de categoría 'velero'. | Alta |
| RF-18 | Una reserva puede cancelarse solo si está en estado PENDIENTE DE PAGO. | Baja |
| RF-19 | Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario. | Alta |
| RF-20 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email. | Alta |
| RF-21 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta. | Baja |
| RF-22 | El administrador puede cambiar el estado de una reserva desde el panel de reservas. | Baja |
| RF-23 | El cliente puede gestionar sus reserva mediante la consulta y cambio del estado. | Alta |
| RF-24 | La interfaz de usuario está íntegramente en español. | Baja |
| RF-25 | El código del sistema está escrito en inglés con comentarios y docstrings en español. | Alta |
| RF-26 | La aplicación funciona en la zona horaria Europe/Madrid y locale español. | Baja |
| RF-27 | Las contraseñas son almacenadas de manera segura con el mecanismo estándar de Django. | Alta |
| RF-28 | La aplicación aplica un CSRF activo y realiza validación de formularios. | Baja |
| RF-29 | El sistema arranca con datos precargados que incluyen 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (una de ellas 'velero'), y 1 usuario administrador y 1 cliente. | Alta |

## Requisitos no funcionales

Total: **5**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Framework | La aplicación se construye con Django 3.2. | Alta |
| RNF-02 | Base de datos | Se utiliza SQLite como base de datos. | Alta |
| RNF-03 | Pasarela de pago | Utiliza PayPal Sandbox como pasarela de pago para pruebas. | Alta |
| RNF-04 | Empaquetado | La aplicación se entrega en un contenedor Docker con instrucciones incluidas en README. | Alta |
| RNF-05 | Zona horaria y locale | Se ejecuta con la zona horaria Europe/Madrid y locale español. | Alta |
