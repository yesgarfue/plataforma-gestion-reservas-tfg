---
run_id: run_2026-05-11_13-31
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-11T13:37:28+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-11_13-31`

## Requisitos funcionales

Total: **19**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El cliente puede reservar un barco sin registro previo. | Media |
| RF-05 | El cliente debe poder iniciar sesión durante el proceso de reserva con recuperación de cesta. | Media |
| RF-06 | El administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La aplicación debe mostrar un catálogo de barcos organizado por categorías. | Alta |
| RF-08 | Los barcos en el catálogo deben marcarse como 'No disponibles' si están fuera del rango de fechas seleccionado. | Alta |
| RF-09 | El cliente debe poder seleccionar la cantidad de unidades del barco y añadirla a la cesta. | Alta |
| RF-10 | La cesta debe estar siempre visible desde cualquier página de la aplicación. | Alta |
| RF-11 | El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta. | Alta |
| RF-12 | El usuario puede finalizar la compra desde la cesta. | Alta |
| RF-13 | La compra se realiza en no más de tres pasos, sin exigir registro previo. | Alta |
| RF-14 | Dos métodos de pago disponibles: PayPal Sandbox y contra-reembolso. | Alta |
| RF-15 | Al finalizar, el cliente recibe un correo electrónico con los datos del barco reservado, el rango de fechas, el importe total y un código de seguimiento. | Alta |
| RF-16 | La reserva debe tener uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO. | Alta |
| RF-17 | Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO. | Alta |
| RF-18 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email. | Alta |
| RF-19 | El administrador puede gestionar barcos, clientes y reservas desde panel propio. | Alta |

## Requisitos no funcionales

Total: **6**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Framework | Se debe utilizar el framework Django 3.2. | Alta |
| RNF-02 | Base de Datos | Se debe utilizar la base de datos SQLite. | Alta |
| RNF-03 | Pasarela de Pago | La pasarela de pago debe ser PayPal Sandbox. | Alta |
| RNF-04 | Empaquetado | La aplicación debe entregarse como contenedor Docker, con instrucciones de construcción y arranque en un README. | Alta |
| RNF-05 | Zona Horaria y Locale | La aplicación debe tener europe/Madrid como zona horaria y el locale en español. | Alta |
| RNF-06 | Seguridad | Las contraseñas no deben almacenarse en texto plano. | Alta |
