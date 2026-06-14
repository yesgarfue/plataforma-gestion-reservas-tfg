---
run_id: run_2026-05-13_15-33
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-13T15:43:23+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-13_15-33`

## Requisitos funcionales

Total: **35**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El registro de cliente es opcional para la reserva. | Alta |
| RF-05 | El inicio de sesión puede realizarse durante el proceso de reserva. | Media |
| RF-06 | Un administrador puede eliminar un usuario cliente si no tiene reservas pendientes. | Alta |
| RF-07 | La página principal muestra catálogo de barcos organizado por categorías. | Alta |
| RF-08 | Cada barco tiene los campos: nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día. | Alta |
| RF-09 | Búsqueda disponible en la página de inicio. | Alta |
| RF-10 | La búsqueda funciona por nombre o título del barco. | Alta |
| RF-11 | Filtros combinables disponibles: puertos, fabricantes, precio, categoría y capacidad. | Alta |
| RF-12 | El filtro de puertos, fabricante y precio se presentan como desplegables. | Media |
| RF-13 | El filtro de fechas muestra todos los barcos del catálogo: los no disponibles en ese rango aparecen marcados con una etiqueta 'No disponible'. | Alta |
| RF-14 | Se puede seleccionar la cantidad de unidades del barco desde la ficha y añadir a la cesta. | Alta |
| RF-15 | La cesta siempre está visible desde cualquier página de la aplicación. | Alta |
| RF-16 | El usuario puede ampliar y reducir la cantidad de unidades de cada barco en la cesta. | Alta |
| RF-17 | El usuario puede revisar el estado de la cesta desde el catálogo. | Media |
| RF-18 | Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir al carro. | Alta |
| RF-19 | El usuario puede finalizar la compra (proceso de reserva). | Alta |
| RF-20 | La compra se realiza en no más de tres pasos, sin exigir registro previo. | Alta |
| RF-21 | Durante el proceso se solicitan los datos del cliente y los datos de pago. | Alta |
| RF-22 | Dos métodos de pago disponibles: PayPal Sandbox y contra-reembolso. | Baja |
| RF-23 | Al finalizar, el cliente recibe un correo electrónico con los datos del barco reservado, el rango de fechas, el importe total y un código de seguimiento. | Alta |
| RF-24 | Los alquileres se miden por día. | Baja |
| RF-25 | Se aplica una tasa de combustible de 50 € por día, excepto si el barco es de categoría 'velero'. | Alta |
| RF-26 | Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO. | Alta |
| RF-27 | Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO. | Alta |
| RF-28 | Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario. | Alta |
| RF-29 | El administrador puede cambiar el estado de una reserva desde el panel de reservas. | Alta |
| RF-30 | El cliente puede consultar el estado de su reserva usando el código de seguimiento. | Alta |
| RF-31 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |
| RF-32 | El administrador puede consultar el estado de cualquier reserva. | Baja |
| RF-33 | Panel de administración propio de la aplicación. | Alta |
| RF-34 | Gestión de barcos (alta, edición, baja). | Baja |
| RF-35 | El usuario puede seleccionar una cantidad de unidades del barco desde la ficha y añadir a la cesta. | Alta |

## Requisitos no funcionales

Total: **8**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Lenguaje | La aplicación se desarrolla en Python 3.2. | Alta |
| RNF-02 | Framework web | Se utiliza Django 3.2 como framework web. | Alta |
| RNF-03 | Base de datos | La base de datos utilizar es SQLite. | Alta |
| RNF-04 | Pasarela de pago | Se utiliza la pasarela de PayPal Sandbox para pagos en línea. | Baja |
| RNF-05 | Empaquetado | La aplicación se empaqueta como contenedor Docker con instrucciones de construcción y arranque incluidas en un README. | Alta |
| RNF-06 | Zona horaria y locale | La aplicación opera con zona horaria Europe/Madrid y locale español. | Alta |
| RNF-07 | Seguridad mínima | Contraseñas no almacenadas en texto plano; CSRF activo; validación de formularios. | Media |
| RNF-08 | Datos seed precargados | La aplicación arranca con datos precargados que permiten probar todas las funcionalidades sin trabajo previo del usuario. | Alta |
