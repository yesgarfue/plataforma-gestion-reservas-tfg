---
run_id: run_2026-05-07_20-50
fase: 01_requisitos
agente: Analista
modelo: ollama/qwen2.5-coder:7b
timestamp: 2026-05-07T21:01:52+02:00
hash_brief: sha256:e62bcd5b2a4f5684...
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-07_20-50`

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
| RF-08 | Los barcos en el catálogo deben permitir la búsqueda por nombre o título. | Alta |
| RF-09 | Los filtros de puerto, fabricante, precio, categoría y capacidad deben estar disponibles y aplicables simultáneamente y de forma independiente. | Alta |
| RF-10 | Los barcos agotados o no disponibles deben aparecer claramente marcados con etiquetas 'No disponible'. | Media |
| RF-11 | El cliente puede ver la ficha del barco desde el catálogo y seleccionar la cantidad de unidades. | Alta |
| RF-12 | El cliente puede ampliar o reducir la cantidad de unidades de cada barco en la cesta. | Alta |
| RF-13 | El cliente puede revisar el estado de la cesta desde el catálogo. | Alta |
| RF-14 | Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir al carro. | Alta |
| RF-15 | El cliente puede finalizar la compra (proceso de reserva) desde la cesta. | Alta |
| RF-16 | La compra se realiza en no más de tres pasos sin exigir registro previo. | Alta |
| RF-17 | Dos métodos de pago disponibles: PayPal Sandbox y contra-reembolso. | Alta |
| RF-18 | Al finalizar, el cliente recibe un correo electrónico con los datos del barco reservado, el rango de fechas, el importe total y un código de seguimiento del alquiler. | Alta |
| RF-19 | Los alquileres se miden por día. | Baja |
| RF-20 | Se aplica una tasa de combustible de 50 € por día, salvo que el barco sea de categoría 'velero', en cuyo caso la tasa es 0 €. | Alta |
| RF-21 | Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO. | Alta |
| RF-22 | Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario. | Media |
| RF-23 | El administrador puede cambiar el estado de una reserva desde el panel de reservas. | Alta |
| RF-24 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email. | Alta |
| RF-25 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |
| RF-26 | El administrador puede consultar el estado de cualquier reserva. | Alta |
| RF-27 | El panel de administración es propio de la aplicación. | Alta |
| RF-28 | El panel de administración permite gestionar barcos (alta, edición, baja). | Alta |
| RF-29 | El panel de administración permite gestionar clientes (consulta, eliminación). | Alta |
| RF-30 | El panel de administración permite gestionar reservas (consulta, cambio de estado). | Alta |

## Requisitos no funcionales

Total: **7**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Lenguaje y Framework | El sistema está construido con Python y Django 3.2. | Alta |
| RNF-02 | Base de Datos | La base de datos está implementada con SQLite. | Alta |
| RNF-03 | Pasarela de Pago | La pasarela de pago es PayPal Sandbox. | Alta |
| RNF-04 | Empaquetado Docker | La aplicación debe entregarse como contenedor Docker. | Alta |
| RNF-05 | Zona Horaria y Locale | La zona horaria es Europe/Madrid y el locale es español. | Alta |
| RNF-06 | Seguridad | La interfaz de usuario está íntegramente en español. | Alta |
| RNF-07 | Usabilidad | La interfaz de usuario está íntegramente en español. | Alta |
