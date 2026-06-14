---
run_id: run_2026-05-12_15-34
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-12T15:52:58+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-12_15-34`

## Requisitos funcionales

Total: **20**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El registro de cliente es opcional para realizar una reserva sin haberse registrado. | Baja |
| RF-05 | El inicio de sesión puede realizarse durante el proceso de reserva; si el usuario tiene una cesta con barcos y decide iniciar sesión, al volver a la página de login debe recuperar la cesta y continuar el proceso. | Alta |
| RF-06 | Un administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La página principal debe mostrar el catálogo de barcos organizado por categorías, mostrando todos los barcos del catálogo con una etiqueta 'No disponible' para aquellos que no están disponibles en ese rango. | Alta |
| RF-08 | El cliente puede realizar una búsqueda por nombre o título de algún barco. | Alta |
| RF-09 | Los filtros combinables son puertos, fabricantes, precio y cantidad, que pueden aplicarse simultáneamente y de forma independiente en el filtrado del catálogo. | Alta |
| RF-10 | Desde la ficha del barco, el cliente puede seleccionar la cantidad de unidades del barco que desea reservar y añadirla a su cesta. | Alta |
| RF-11 | La cesta está siempre visible desde cualquier página de la aplicación. El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta, y revisar el estado de su cesta desde el catálogo. | Alta |
| RF-12 | Al entrar en modo administrador, la cesta se vacía y este último no puede añadir al carro, aunque puede revisar el estado de su cesta. | Alta |
| RF-13 | La compra debe realizarse en tres pasos sin necesidad de registro previo y se deben solicitar los datos del cliente (directamente o heredados si hay sesión iniciada) junto con los datos de pago. | Alta |
| RF-14 | Se ofrece el método de pago PayPal Sandbox y contra-reembolso para la compra del alquiler. | Alta |
| RF-15 | El cliente recibe un correo electrónico con los datos del barco reservado, el rango de fechas, el importe total y el código de seguimiento del alquiler. | Alta |
| RF-16 | Las tasa de combustible se aplica siempre en 50 € por día, salvo que la categoría del barco sea 'velero', donde esta tasa es de 0 €. | Alta |
| RF-17 | Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO. Un recordatorio por email se enviará al usuario si falta un día de inicio de la reserva. | Alta |
| RF-18 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email, incluso si no está registrado. | Alta |
| RF-19 | El usuario registrado puede consultar la historia de sus reservas desde su cuenta. | Alta |
| RF-20 | El administrador puede gestionar las reservas, verla y cambiar su estado (siempre que esté en PENDIENTE DE PAGO). | Alta |

## Requisitos no funcionales

Total: **7**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Framework Web | Se debe utilizar Django 3.2 como framework web. | Alta |
| RNF-02 | Base de Datos | El sistema debe emplear SQLite como base de datos. | Alta |
| RNF-03 | Pasarela de Pago | Se debe usar PayPal Sandbox para los pagos, no la pasarela de pago en producción. | Alta |
| RNF-04 | Empaquetado | La aplicación debe entregarse como un contenedor Docker con instrucciones de construcción y arranque en el README. | Alta |
| RNF-05 | Zona Horaria y Locale | El sistema debe operar bajo la zona horaria Europe/Madrid con locale español. | Alta |
| RNF-06 | Seguridad | Contraseñas no deben almacenarse en texto plano y el sistema debe activar CSRF al realizar formularios. | Alta |
| RNF-07 | Datos Seed | La aplicación debe arrancar con 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (una de ella 'velero'), un usuario administrador y un usuario cliente. | Alta |
