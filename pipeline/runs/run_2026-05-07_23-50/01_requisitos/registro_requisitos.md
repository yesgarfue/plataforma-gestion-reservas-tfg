---
run_id: run_2026-05-07_23-50
fase: 01_requisitos
agente: Analista
modelo: ollama/qwen2.5-coder:7b
timestamp: 2026-05-07T23:57:27+02:00
hash_brief: sha256:e62bcd5b2a4f5684...
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-07_23-50`

## Requisitos funcionales

Total: **21**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El cliente puede reservar un barco sin registro previo. | Media |
| RF-05 | El cliente debe poder iniciar sesión durante el proceso de reserva con recuperación de cesta. | Media |
| RF-06 | El administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La aplicación debe mostrar un catálogo de barcos organizado por categorías. | Alta |
| RF-08 | Los barcos en el catálogo deben permitir la búsqueda por nombre o título. | Alta |
| RF-09 | Los filtros de puerto, fabricante, precio, categoría y capacidad deben permitirse aplicarse simultáneamente y de forma independiente en los resultados de búsqueda. | Alta |
| RF-10 | El cliente debe poder seleccionar la cantidad de unidades del barco. | Alta |
| RF-11 | El cliente debe poder añadir el barco a la cesta. | Alta |
| RF-12 | La cesta debe estar siempre visible desde cualquier página de la aplicación. | Alta |
| RF-13 | El usuario debe poder ampliar o reducir la cantidad de unidades en la cesta. | Alta |
| RF-14 | El usuario puede finalizar la compra desde la cesta, realizando el proceso de reserva en no más de tres pasos. | Alta |
| RF-15 | Se debe aplicar una tasa de combustible de 50 € por día para los barcos no de categoría 'velero'. | Alta |
| RF-16 | Los alquileres deben tener uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO. | Alta |
| RF-17 | Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO. | Alta |
| RF-18 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email. | Alta |
| RF-19 | El administrador puede cambiar el estado de una reserva desde el panel de reservas. | Alta |
| RF-20 | El cliente registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |
| RF-21 | El panel de administración debe permitir la gestión de barcos, clientes y reservas. | Alta |

## Requisitos no funcionales

Total: **8**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Lenguaje | La aplicación se desarrolla en Python. | Alta |
| RNF-02 | Framework web | Se utiliza Django 3.2. | Alta |
| RNF-03 | Base de datos | Se utiliza SQLite. | Alta |
| RNF-04 | Pasarela de pago | Se utiliza PayPal Sandbox. | Alta |
| RNF-05 | Empaquetado | La aplicación debe entregarse como contenedor Docker. | Alta |
| RNF-06 | Zona horaria y locale | La aplicación debe ejecutarse con la zona horaria Europe/Madrid y el locale español. | Alta |
| RNF-07 | Seguridad | Las contraseñas están almacenadas en texto plano. | Baja |
| RNF-08 | Datos seed | El sistema debe arrancar con datos precargados que permitan probar todas las funcionalidades. | Alta |
