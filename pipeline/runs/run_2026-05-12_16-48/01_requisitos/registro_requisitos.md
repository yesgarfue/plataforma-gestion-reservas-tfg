---
run_id: run_2026-05-12_16-48
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-12T16:59:25+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-12_16-48`

## Requisitos funcionales

Total: **37**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El registro de cliente es opcional para la reserva sin registro previo. | Alta |
| RF-05 | El inicio de sesión puede realizarse durante el proceso de reserva, reconstrayendo la cesta. | Alta |
| RF-06 | Un administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La página principal muestra un catálogo de barcos organizado por categorías. | Alta |
| RF-08 | Los barcos tienen los campos: nombre, imagen (una imagen obligatoria), categoría, fabricante, puerto, capacidad y precio por día. | Alta |
| RF-09 | Se puede buscar en la página principal por nombre o título de barco. | Alta |
| RF-10 | Los filtros combinables son puertos, fabricantes, precio, categoría, capacidad y rango de fechas. | Alta |
| RF-11 | El filtro por puerto y fabricante se presentan como desplegables con valores válidos. | Alta |
| RF-12 | Los barcos agotados o no disponibles aparecen claramente marcados. | Alta |
| RF-13 | La ficha del barco muestra los datos del barco y la imagen. | Alta |
| RF-14 | Desde la ficha, el cliente puede seleccionar la cantidad de unidades del barco. | Alta |
| RF-15 | El administrador dispone de su propia ficha de barco con acciones de gestión (alta, edición, baja). | Alta |
| RF-16 | La cesta está siempre visible desde cualquier página de la aplicación. | Alta |
| RF-17 | El usuario puede ampliar o reducir la cantidad de unidades en la cesta. | Alta |
| RF-18 | El administrador no puede añadir al carro cuando entra en modo administrador, y la cesta se vacía. | Alta |
| RF-19 | El usuario puede revisar el estado de la cesta desde el catálogo. | Alta |
| RF-20 | Desde la cesta, el usuario puede finalizar la compra (proceso de reserva). | Alta |
| RF-21 | La compra se realiza en no más de tres pasos sin exigir registro previo. | Alta |
| RF-22 | Se solicitan los datos del cliente y los datos de pago durante el proceso de reserva. | Alta |
| RF-23 | Dos métodos de pago disponibles: PayPal Sandbox y contra-reembolso. | Alta |
| RF-24 | El cliente recibe un correo electrónico con los datos del barco reservado, el rango de fechas y el código de seguimiento. | Alta |
| RF-25 | Los alquileres se miden por día. | Alta |
| RF-26 | Se aplica una tasa de combustible de 50 €/día para los barcos no de categoría 'velero'. | Alta |
| RF-27 | Para los barcos de la categoría 'velero', no se aplica ninguna tasa de combustible. | Alta |
| RF-28 | Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO. | Alta |
| RF-29 | Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO. | Alta |
| RF-30 | Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, se envía un correo recordatorio al usuario. | Alta |
| RF-31 | El administrador puede cambiar el estado de una reserva desde el panel de reservas (botón por transición). | Alta |
| RF-32 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido. | Alta |
| RF-33 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |
| RF-34 | Gestión administrativa tiene acceso al panel propio para la aplicación (diferente del admin de Django por defecto). | Alta |
| RF-35 | El panel de administración permite gestionar los barcos (alta, edición, baja). | Alta |
| RF-36 | El panel de administración permite gestionar los clientes (consulta, eliminación). | Alta |
| RF-37 | El panel de administración permite gestionar las reservas (consulta, cambio de estado). | Alta |

## Requisitos no funcionales

Total: **8**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Idioma | La interfaz de usuario está íntegramente en español. | Alta |
| RNF-02 | Framework web | Se usa Django 3.2 como framework web. | Alta |
| RNF-03 | Base de datos | Usa SQLite como base de datos. | Alta |
| RNF-04 | Pasarela de pago | Se utiliza PayPal Sandbox para el proceso de pago en despliegue local. | Alta |
| RNF-05 | Empaquetado y despliegue | La aplicación se empaqueta y entrega como contenedor Docker, incluyendo instrucciones en un README. | Alta |
| RNF-06 | Zona horaria y locale | La aplicación opera la fecha horaria en Europe/Madrid con sistema de localización español. | Alta |
| RNF-07 | Seguridad minimal | Las contraseñas no están almacenadas en texto plano y se aplica CSRF activo. | Alta |
| RNF-08 | Datos seed precargados | La aplicación arranca con datos pre-cargados para probar todas las funcionalidades de manera automática. | Alta |
