---
run_id: run_2026-05-09_18-54
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-09T19:02:05+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-09_18-54`

## Requisitos funcionales

Total: **30**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El cliente puede reservar un barco sin registro previo. | Media |
| RF-05 | El cliente debe poder iniciar sesión durante el proceso de reserva con recuperación de cesta. | Media |
| RF-06 | El administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La aplicación debe mostrar un catálogo de barcos organizado por categorías. | Alta |
| RF-08 | Los barcos en el catálogo deben presentar campos: nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día. | Media |
| RF-09 | El sistema debe permitir la búsqueda por nombre o título del barco. | Media |
| RF-10 | El sistema debe permitir la búsqueda por puertos, fabricantes, precio, categoría, capacidad y rango de fechas simultáneamente y de forma independiente en el catálogo de barcos. | Alta |
| RF-11 | El cliente puede navegar por el catálogo de barcos mediante filtros. | Media |
| RF-12 | Debería estar disponible una ficha de barco accesible desde el catálogo, con los datos del barco y la imagen. | Alta |
| RF-13 | De la ficha de barco, el cliente puede seleccionar la cantidad de unidades del barco y añadir a la cesta. | Media |
| RF-14 | El cesta debe estar visible desde cualquier página de la aplicación, y permite modificar la cantidad de unidades de cada barco. | Alta |
| RF-15 | La cesta debe vaciarse al entrar en modo administrador. | Alta |
| RF-16 | El cliente puede finalizar la compra (proceso de reserva) desde la cesta. | Media |
| RF-17 | El proceso de reserva debe completarse en no más de tres pasos. | Alta |
| RF-18 | Se deben proporcionar dos métodos de pago: PayPal Sandbox y contra-reembolso. | Alta |
| RF-19 | Al finalizar, el cliente debe recibir un correo electrónico con el código de seguimiento del alquiler y los datos del barco reservado. | Alta |
| RF-20 | El sistema debe aplicar una tasa de combustible de 50 € por día, salvo que el barco sea de categoría 'velero', en cuyo caso la tasa es 0 €. | Alta |
| RF-21 | Cada reserva debe tener uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO. | Alta |
| RF-22 | Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO. | Alta |
| RF-23 | El sistema debe enviar un correo de recordatorio al usuario 24 horas antes de la reserva si sigue en estado PENDIENTE DE PAGO. | Alta |
| RF-24 | El administrador puede cambiar el estado de una reserva desde el panel de reservas. | Alta |
| RF-25 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email. | Media |
| RF-26 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |
| RF-27 | El administrador puede consultar el estado de cualquier reserva. | Alta |
| RF-28 | El panel de administración debe permitir la gestión de barcos (alta, edición, baja). | Alta |
| RF-29 | El panel de administración debe permitir la gestión de clientes (consulta, eliminación con la restricción del 3.1). | Alta |
| RF-30 | El panel de administración debe permitir la gestión de reservas (consulta, cambio de estado). | Alta |

## Requisitos no funcionales

Total: **6**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Lenguaje | Se utiliza Python como lenguaje de programación. | Alta |
| RNF-02 | Framework | Se utiliza Django 3.2 como framework web. | Alta |
| RNF-03 | Base de datos | Se utiliza SQLite como base de datos. | Alta |
| RNF-04 | Pasarela de pago | Se utiliza PayPal Sandbox como pasarela de pago. | Alta |
| RNF-05 | Empaquetado | Existe un Dockerfile en el repositorio del producto. | Alta |
| RNF-06 | Idioma | La interfaz de usuario está íntegramente en español. | Alta |
