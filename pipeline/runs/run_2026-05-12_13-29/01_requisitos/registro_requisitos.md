---
run_id: run_2026-05-12_13-29
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-12T13:47:55+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-12_13-29`

## Requisitos funcionales

Total: **24**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El registro de cliente es opcional para realizar una reserva sin haberse registrado. | Baja |
| RF-05 | El inicio de sesión puede realizarse durante el proceso de reserva manteniendo la cesta. | Media |
| RF-06 | Un administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La página principal muestra un catálogo de barcos organizado por categorías. | Alta |
| RF-08 | Los barcos tienen los campos: nombre, imagen (una imagen obligatoria), categoría, fabricante, puerto, capacidad y precio por día. | Alta |
| RF-09 | La búsqueda está disponible en la página de inicio, acepta búsquedas por nombre o título del barco y aplica filtros combinables. | Alta |
| RF-10 | Los barcos agotados o no disponibles son claramente marcados en el catálogo. | Baja |
| RF-11 | Se puede seleccionar la cantidad de unidades del barco desde la ficha y añadir a la cesta. | Alta |
| RF-12 | La cesta está siempre visible desde cualquier página de la aplicación. | Alta |
| RF-13 | El usuario puede aumentar o reducir la cantidad de unidades de cada barco en la cesta. | Media |
| RF-14 | Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir al carro. | Alta |
| RF-15 | La compra puede completarse en un proceso de tres pasos sin necesidad de registro previo. | Alta |
| RF-16 | Se ofrece dos métodos de pago: PayPal Sandbox y contra-reembolso. | Alta |
| RF-17 | El cliente recibe un correo electrónico con los datos del barco reservado, rango de fechas, importe total y código de seguimiento. | Alta |
| RF-18 | Se aplica una tasa de combustible de 50 € por día, salvo para los veleros donde no hay tasa. | Alta |
| RF-19 | Una reserva puede cancelarse solo si está en estado PENDIENTE DE PAGO y es eliminada del sistema. | Alta |
| RF-20 | Se envía un correo de recordatorio al usuario una día antes del inicio de la reserva cuando esta sigue en estado PENDIENTE DE PAGO. | Baja |
| RF-21 | El administrador puede cambiar el estado de una reserva desde el panel de reservas para transiciones aplicables. | Alta |
| RF-22 | La consulta del estado de la reserva se realiza usando el código de seguimiento recibido por email, incluso si el cliente no está registrado. | Alta |
| RF-23 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta en el sistema. | Alta |
| RF-24 | El administrador puede consultar el estado de cualquier reserva. | Alta |

## Requisitos no funcionales

Total: **7**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Lenguaje y framework | La aplicación se desarrolla con Python y basada en Django 3.2. | Alta |
| RNF-02 | Base de datos | Se utiliza SQLite como base de datos. | Alta |
| RNF-03 | Pasarela de pago | Se utiliza la pasarela de pago PayPal Sandbox para pruebas. | Alta |
| RNF-04 | Empaquetado | La aplicación debe ser entregada como contenedor Docker con instrucciones de construcción y arranque en un README. | Alta |
| RNF-05 | Zona horaria y locale | La aplicación debe funcionar bajo la zona horaria Europe/Madrid y locale español. | Alta |
| RNF-06 | Seguridad mínima | Las contraseñas no están almacenadas en texto plano; CSRF activo; validación de formularios. | Alta |
| RNF-07 | Datos seed precargados | La aplicación debe arrancar con datos precargados (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, 1 usuario administrador y 1 cliente). | Alta |
