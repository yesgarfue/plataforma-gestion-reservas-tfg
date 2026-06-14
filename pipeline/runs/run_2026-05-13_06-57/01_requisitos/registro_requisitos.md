---
run_id: run_2026-05-13_06-57
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-13T07:06:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-13_06-57`

## Requisitos funcionales

Total: **26**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El registro de cliente es opcional: puede reservar sin registrarse. | Alta |
| RF-05 | El inicio de sesión durante el proceso de reserva recupera la cesta del usuario y continúa con el proceso. | Alta |
| RF-06 | El administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La página principal presenta el catálogo de barcos organizado por categorías. | Alta |
| RF-08 | Se permite búsqueda en la página de inicio por nombre o título del barco. | Alta |
| RF-09 | Los filtros combinables son puertos, fabricantes, precio, categoría, capacidad y rango de fechas. | Alta |
| RF-10 | El filtro de puertos y fabricante se presentan como desplegables con valores válidos. | Alta |
| RF-11 | Los barcos no disponibles en el rango seleccionado aparecen marcados con una etiqueta 'No disponible'. | Alta |
| RF-12 | El cliente puede acceder a la ficha del barco desde el catálogo, incluyendo cantidad y selección para la cesta. | Alta |
| RF-13 | La cesta siempre está visible e interactiva desde cualquier página de la aplicación. | Alta |
| RF-14 | El usuario puede ampliar o reducir la cantidad de unidades de cada barco en el carrito de compras. | Alta |
| RF-15 | La cesta del administrador se vacía automáticamente al entrar como admin y no permite añadir productos. | Alta |
| RF-16 | Pasa el proceso de reserva en tres pasos, sin exigir registro previo. | Alta |
| RF-17 | Se presentan dos métodos de pago: PayPal Sandbox y contra-reembolso. | Alta |
| RF-18 | El cliente recibe un correo electrónico con los datos del barco reservado, el rango de fechas y la información total del alquiler. | Alta |
| RF-19 | Se aplica una tasa de combustible de 50 € por día, excepto para los barcos en la categoría 'velero'. | Alta |
| RF-20 | Las reservas tienen cuatro estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO. | Alta |
| RF-21 | Se puede cancelar una reserva únicamente si está en estado PENDIENTE DE PAGO. | Alta |
| RF-22 | Se envía un correo de recordatorio al cliente una día antes de la fecha de inicio de la reserva, siempre que la reserva esté en estado PENDIENTE DE PAGO. | Alta |
| RF-23 | El administrador puede cambiar el estado de una reserva desde el panel propio. | Alta |
| RF-24 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por correo electrónico. | Alta |
| RF-25 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta personal. | Alta |
| RF-26 | El administrador puede consultar el estado de cualquier reserva en la aplicación. | Alta |

## Requisitos no funcionales

Total: **9**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Lenguaje y framework | Se utiliza Python como lenguaje de programación. | Alta |
| RNF-02 | Framework web | Se utiliza Django 3.2 como framework web. | Alta |
| RNF-03 | Base de datos | El sistema utiliza SQLite como base de datos. | Alta |
| RNF-04 | Pasarela de pago | La aplicación utilizas PayPal Sandbox para el proceso de pago en desarrollo. | Alta |
| RNF-05 | Empaquetado Docker | La aplicación se debe empaquetar y ejecutar como contenedor Docker. | Alta |
| RNF-06 | Zona horaria | El sistema opera bajo una zona horaria de 'Europe/Madrid'. | Media |
| RNF-07 | Locale y idioma | La interfaz del usuario está íntegramente en español. | Alta |
| RNF-08 | Seguridad mínima | Las contraseñas están almacenadas de forma segura utilizando el mecanismo estándar de Django y se activa la protección CSRF. | Alta |
| RNF-09 | Datos seed | La aplicación debe arrancar con predefinidos 5 barcos, 2 puertos, 2 fabricantes, 2 categorías y 1 usuario administrador y cliente. | Alta |
