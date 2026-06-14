---
run_id: run_2026-05-08_12-03
fase: 01_requisitos
agente: Analista
modelo: ollama/qwen2.5-coder:7b
timestamp: 2026-05-08T12:11:01+02:00
hash_brief: sha256:e62bcd5b2a4f5684...
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-08_12-03`

## Requisitos funcionales

Total: **28**

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
| RF-10 | El cliente debe poder seleccionar la cantidad de unidades de un barco en la ficha de barco y añadirlo a la cesta. | Alta |
| RF-11 | La cesta se debe mantener visible en cualquier página de la aplicación. | Alta |
| RF-12 | El cliente debe poder aumentar, disminuir o eliminar la cantidad de unidades de un barco en la cesta. | Alta |
| RF-13 | El administrador, al entrar en modo administrador, debe tener la cesta vacía y no podrá añadir al carro. | Alta |
| RF-14 | El cliente debe poder finalizar la compra desde la cesta. | Alta |
| RF-15 | El proceso de reserva debe realizarse en no más de tres pasos: selección de barco, datos de contacto y pago. | Alta |
| RF-16 | Se deben proporcionar dos métodos de pago: PayPal Sandbox y contra-reembolso. | Alta |
| RF-17 | Al finalizar la compra, el cliente debe recibir un correo electrónico con los datos del barco reservado, el rango de fechas, el importe total y un código de seguimiento del alquiler. | Alta |
| RF-18 | Se debe aplicar una tasa de combustible de 50 € por día, salvo que el barco sea de categoría 'velero', en cuyo caso la tasa es 0 €. | Alta |
| RF-19 | Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO. No existe un estado CANCELADO. | Alta |
| RF-20 | Únicamente una reserva en estado PENDIENTE DE PAGO puede ser cancelada, implica su eliminación del sistema. | Alta |
| RF-21 | Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema debe enviar un correo de recordatorio al usuario. | Alta |
| RF-22 | El administrador, desde el panel de reservas, debe tener la opción de cambiar el estado de una reserva. | Alta |
| RF-23 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email. | Alta |
| RF-24 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |
| RF-25 | El administrador puede consultar el estado de cualquier reserva. | Alta |
| RF-26 | El panel de administración propio de la aplicación debe permitir la gestión de barcos (alta, edición, baja). | Alta |
| RF-27 | El panel de administración propio de la aplicación debe permitir la gestión de clientes (consulta, eliminación con la restricción del 3.1). | Alta |
| RF-28 | El panel de administración propio de la aplicación debe permitir la gestión de reservas (consulta, cambio de estado). | Alta |

## Requisitos no funcionales

Total: **6**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Lenguaje y framework | La aplicación se desarrolla en Python con el framework Django 3.2. | Alta |
| RNF-02 | Base de datos | Se utiliza SQLite como base de datos. | Alta |
| RNF-03 | Pasarela de pago | Se utiliza la Pasarela de pago en entorno Sandbox de PayPal. | Alta |
| RNF-04 | Empaquetado | La aplicación debe ser empaquetada como contenedor Docker con instrucciones en un README. | Alta |
| RNF-05 | Zona horaria y locale | La aplicación debe estar configurada en la zona horaria de Madrid y utilizar el idioma español. | Alta |
| RNF-06 | Seguridad | La aplicación debe cumplir con las recomendaciones de seguridad para la autenticación y el manejo de datos de pago. | Media |
