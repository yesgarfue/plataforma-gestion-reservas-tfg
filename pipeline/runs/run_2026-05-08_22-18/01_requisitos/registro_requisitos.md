---
run_id: run_2026-05-08_22-18
fase: 01_requisitos
agente: Analista
modelo: ollama/hundidos-analista:latest
timestamp: 2026-05-08T22:36:34+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 1
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-08_22-18`

## Requisitos funcionales

Total: **29**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El cliente puede reservar un barco sin registro previo. | Alta |
| RF-05 | El sistema recoge los datos mínimos necesarios durante el proceso de reserva de un cliente no registrado. | Alta |
| RF-06 | El cliente puede iniciar sesión durante el proceso de reserva. | Alta |
| RF-07 | Al iniciar sesión, el cliente puede recuperar la cesta y continuar el proceso de reserva. | Alta |
| RF-08 | Un administrador puede eliminar un usuario cliente si no tiene reservas pendientes. | Alta |
| RF-09 | La página principal muestra el catálogo de barcos organizado por categorías. | Alta |
| RF-10 | Cada barco tiene los campos: nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día. | Alta |
| RF-11 | El cliente puede buscar barcos por nombre o título. | Alta |
| RF-12 | Los filtros combinables (puertos, fabricantes, precio, categoría, capacidad y rango de fechas) son presentados como desplegables con valores válidos y pueden aplicarse simultáneamente y de forma independiente. | Alta |
| RF-13 | Los filtros de puerto y fabricante no ocultan los barcos no disponibles en el rango seleccionado. | Alta |
| RF-14 | Los barcos agotados o no disponibles aparecen claramente marcados. | Alta |
| RF-15 | El cliente puede seleccionar la cantidad de unidades del barco desde la ficha del barco y añadirla a la cesta. | Alta |
| RF-16 | El formulario de pago debe solicitar los datos del cliente y los datos de pago. | Alta |
| RF-17 | El cliente recibe un correo electrónico con los datos del barco reservado, el rango de fechas, el importe total y el código de seguimiento del alquiler. | Alta |
| RF-18 | Los alquileres se miden por día. | Alta |
| RF-19 | La tasa de combustible es de 50 € por día, salvo que el barco sea de categoría 'velero', en cuyo caso la tasa es 0 €. | Alta |
| RF-20 | Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO. | Alta |
| RF-21 | Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO. Cancelar una reserva implica su eliminación del sistema. | Alta |
| RF-22 | Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario. | Alta |
| RF-23 | El administrador puede cambiar el estado de una reserva desde el panel de reservas. | Alta |
| RF-24 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email, incluso si no está registrado. | Alta |
| RF-25 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |
| RF-26 | El administrador puede consultar el estado de cualquier reserva. | Alta |
| RF-27 | El panel de administración propio incluye gestionar barcos (alta, edición, baja). | Alta |
| RF-28 | El panel de administración propio incluye gestionar clientes (consulta, eliminación con la restricción del 3.1). | Alta |
| RF-29 | El panel de administración propio incluye gestionar reservas (consulta, cambio de estado). | Alta |

## Requisitos no funcionales

Total: **3**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Seguridad | La interfaz de usuario está íntegramente en español. | Alta |
| RNF-02 | Rendimiento | La aplicación es accesible desde el navegador en la URL documentada. | Alta |
| RNF-03 | Usabilidad | El cliente puede navegar fácilmente por los diferentes elementos y funcionalidades. | Alta |
