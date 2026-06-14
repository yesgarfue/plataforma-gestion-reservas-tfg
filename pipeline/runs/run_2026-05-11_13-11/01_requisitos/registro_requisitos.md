---
run_id: run_2026-05-11_13-11
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-11T13:21:16+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-11_13-11`

## Requisitos funcionales

Total: **33**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El cliente puede reservar un barco sin registro previo. | Media |
| RF-05 | El cliente debe poder iniciar sesión durante el proceso de reserva con recuperación de cesta. | Media |
| RF-06 | El administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La aplicación debe mostrar un catálogo de barcos organizado por categorías. | Alta |
| RF-08 | Los barcos en el catálogo deben presentar nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día. | Alta |
| RF-09 | El cliente debe poder buscar por nombre o título del barco. | Baja |
| RF-10 | Los filtros combinables deben incluir puertos, fabricantes, precio, categoría, capacidad y rango de fechas. | Alta |
| RF-11 | El filtro de puerto y fabricante deben presentarse como desplegables con valores válidos. | Baja |
| RF-12 | Los barcos agotados o no disponibles deben aparecer claramente marcados. | Baja |
| RF-13 | La ficha del barco debe mostrar los datos del barco y la imagen. | Alta |
| RF-14 | El cliente debe poder seleccionar la cantidad de unidades del barco y añadir a la cesta. | Alta |
| RF-15 | El usuario puede revisar el estado de la cesta desde el catálogo. | Baja |
| RF-16 | La cesta debe estar siempre visible desde cualquier página de la aplicación. | Alta |
| RF-17 | El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta. | Alta |
| RF-18 | El administrador, al entrar en modo administrador, debe vaciar la cesta y no poder añadir al carro. | Alta |
| RF-19 | El usuario puede finalizar la compra (proceso de reserva), realizando no más de tres pasos sin exigir registro. | Alta |
| RF-20 | El proceso de reserva debe permitir el pago mediante PayPal Sandbox y contra-reembolso. | Alta |
| RF-21 | Al finalizar la compra, el cliente debe recibir un correo electrónico con los datos del barco reservado, el rango de fechas, el importe total y un código de seguimiento del alquiler. | Alta |
| RF-22 | Los alquileres se miden por día. | Baja |
| RF-23 | Se aplica una tasa de combustible de 50 € por día, salvo para veleros. | Alta |
| RF-24 | Cada reserva debe tener uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO. | Alta |
| RF-25 | Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO. | Alta |
| RF-26 | Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema debe enviar un correo de recordatorio al usuario. | Media |
| RF-27 | El administrador puede cambiar el estado de una reserva desde el panel de reservas. | Alta |
| RF-28 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email. | Alta |
| RF-29 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |
| RF-30 | El administrador puede consultar el estado de cualquier reserva. | Alta |
| RF-31 | El panel de administración debe permitir la gestión de barcos (alta, edición, baja). | Alta |
| RF-32 | El panel de administración debe permitir la gestión de clientes (consulta, eliminación con la restricción del 3.1). | Alta |
| RF-33 | El panel de administración debe permitir la gestión de reservas (consulta, cambio de estado). | Alta |

## Requisitos no funcionales

Total: **8**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Lenguaje | El lenguaje de codificación es Python. | Alta |
| RNF-02 | Framework | Se utiliza Django 3.2. | Alta |
| RNF-03 | Base de datos | Se utiliza SQLite. | Alta |
| RNF-04 | Pasarela de pago | Se utiliza PayPal Sandbox. | Alta |
| RNF-05 | Empaquetado | La aplicación debe estar empaquetada en un contenedor Docker. | Alta |
| RNF-06 | Zona horaria y locale | La zona horaria es Europe/Madrid y el locale es español. | Alta |
| RNF-07 | Seguridad | Se aplica seguridad mínima recomendada (contraseñas no almacenadas, CSRF activo). | Alta |
| RNF-08 | Datos de ejemplo | La aplicación debe arrancar con datos precargados (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, 1 usuario administrador, 1 usuario cliente). | Alta |
