---
run_id: run_2026-05-09_20-18
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-09T20:26:21+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-09_20-18`

## Requisitos funcionales

Total: **36**

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
| RF-10 | El sistema debe ofrecer filtros combinables por puertos, fabricantes, precio, categoría, capacidad y rango de fechas. | Baja |
| RF-11 | Los filtros presentan valores desplegables y no como campos de texto libre. | Media |
| RF-12 | El sistema debe identificar los barcos no disponibles en el rango solicitado con una etiqueta 'No disponible'. | Media |
| RF-13 | El sistema debe mostrar los barcos agotados o no disponibles claramente marcados. | Media |
| RF-14 | El cliente puede acceder a la ficha del barco desde el catálogo, con los datos del barco y la imagen. | Alta |
| RF-15 | Desde la ficha del barco, el cliente puede seleccionar la cantidad de unidades del barco y añadirlo a la cesta. | Media |
| RF-16 | Se proporciona un panel de administración con acciones de gestión para barcos, clientes y reservas. | Alta |
| RF-17 | El cliente puede finalizar la compra desde la cesta, siguiendo un proceso en tres pasos. | Alta |
| RF-18 | Se ofrecen dos métodos de pago: PayPal Sandbox y contra-reembolso. | Alta |
| RF-19 | Al finalizar la compra, el cliente recibe un correo electrónico con los datos del alquiler, el rango de fechas, el importe total y un código de seguimiento. | Alta |
| RF-20 | Se aplica una tasa de combustible de 50 € por día, salvo que el barco sea de categoría 'velero', en cuyo caso la tasa es 0 €. | Alta |
| RF-21 | Las reservas tienen los estados: 'PENDIENTE DE PAGO', 'PAGADO', 'EN USO', 'DEVUELTO'. | Alta |
| RF-22 | Una reserva puede cancelarse únicamente si está en estado 'PENDIENTE DE PAGO'. | Alta |
| RF-23 | Si falta un día para el inicio de la reserva y sigue en estado 'PENDIENTE DE PAGO', el sistema envía un correo de recordatorio al usuario. | Alta |
| RF-24 | El administrador puede cambiar el estado de una reserva desde el panel de reservas. | Alta |
| RF-25 | El cliente puede consultar el estado de su reserva usando el código de seguimiento. | Alta |
| RF-26 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |
| RF-27 | El cliente puede agregar unidades a la cesta desde la ficha del barco. | Media |
| RF-28 | El cliente puede ajustar la cantidad de unidades en la cesta. | Media |
| RF-29 | Si el usuario entra en modo administrador, la cesta se vacía y no puede añadir al carro. | Alta |
| RF-30 | Se permite la gestión de barcos (alta, edición, baja) desde el panel administrativo. | Alta |
| RF-31 | Se permite la gestión de clientes desde el panel administrativo (consulta, eliminación) | Alta |
| RF-32 | El usuario puede eliminar reservas pendientes desde el panel administrativo. | Alta |
| RF-33 | El usuario puede cambiar su contraseña desde su cuenta personal. | Media |
| RF-34 | El usuario puede cambiar su nombre de contacto desde su cuenta personal. | Media |
| RF-35 | La aplicación debe estar accesible desde el navegador en la URL documentada. | Alta |
| RF-36 | La aplicación es accesible desde el navegador en la URL documentada. | Alta |

## Requisitos no funcionales

Total: **5**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Idioma | La interfaz de usuario está íntegramente en español. | Alta |
| RNF-02 | Tiempo de respuesta | La página principal carga en menos de 5 segundos. | Baja |
| RNF-03 | Seguridad | Los datos del usuario están cifrados en reposo y en tránsito. | Alta |
| RNF-04 | Usabilidad | Los elementos críticos están colocados fácilmente para el usuario. | Baja |
| RNF-05 | Escalabilidad | La aplicación debe soportar un aumento en el número de usuarios sin afectar la performance. | Baja |
