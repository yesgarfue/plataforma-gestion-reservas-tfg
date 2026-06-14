---
run_id: run_2026-05-10_10-50
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-10T10:57:03+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-10_10-50`

## Requisitos funcionales

Total: **20**

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
| RF-10 | El cliente debe poder seleccionar la cantidad de unidades del barco seleccionado y añadirlo a la cesta. | Alta |
| RF-11 | La cesta debe estar siempre visible desde cualquier página de la aplicación. | Alta |
| RF-12 | El administrador debe poder vaciar la cesta cuando entre al modo administrador. | Alta |
| RF-13 | La compra debe realizarse en no más de tres pasos, sin exigir registro previo. | Alta |
| RF-14 | El cliente debe poder finalizar la compra y recibir un correo electrónico con los datos del barco reservado, el rango de fechas, el importe total y el código de seguimiento. | Alta |
| RF-15 | La tasa de combustible de 50 € por día debe aplicarse salvo que el barco sea de categoría 'velero', en cuyo caso la tasa es 0 €. | Alta |
| RF-16 | El estado de reserva debe ser PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO. El estado CANCELADO no existe. | Alta |
| RF-17 | Una reserva en estado PENDIENTE DE PAGO puede ser cancelada únicamente por el administrador. Las reservas canceladas implica su eliminación del sistema. | Alta |
| RF-18 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email, incluso si no está registrado. | Alta |
| RF-19 | El administrador puede cambiar el estado de una reserva desde el panel de reservas (pendiente, pagado, en uso, devuelto). | Alta |
| RF-20 | El cliente registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |

## Requisitos no funcionales

Total: **7**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Lenguaje y framework | El sistema está construido con Python usando Django 3.2. | Alta |
| RNF-02 | Base de datos | La base de datos utilizada es SQLite. | Alta |
| RNF-03 | Pasarela de pago | La pasarela de pago utilizada es PayPal Sandbox. | Alta |
| RNF-04 | Empaquetado | La aplicación debe entregarse como contenedor Docker. | Alta |
| RNF-05 | Zona horaria y locale | El sistema operará bajo la zona horaria Europe/Madrid y el locale español. | Alta |
| RNF-06 | Seguridad | Contraseñas no almacenadas en texto plano y CSRF activo. | Alta |
| RNF-07 | Datos seed | La aplicación debe arrancar con datos precargados de 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (una de ellas 'velero') y 1 usuario administrador de prueba. | Alta |
