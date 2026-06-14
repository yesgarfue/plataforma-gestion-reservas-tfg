---
run_id: run_2026-05-14_16-05
fase: 01_requisitos
agente: Analista
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T16:05:40+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 01 — Registro de requisitos

**ID de ejecución**: `run_2026-05-14_16-05`

## Requisitos funcionales

Total: **38**

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El cliente puede registrarse mediante correo electrónico y contraseña. | Alta |
| RF-02 | El cliente puede iniciar sesión con correo y contraseña. | Alta |
| RF-03 | El cliente puede cerrar sesión explícitamente. | Alta |
| RF-04 | El cliente puede completar una reserva sin haberse registrado previamente. | Alta |
| RF-05 | El cliente puede iniciar sesión durante el proceso de reserva y recuperar su cesta al volver de la página de login. | Alta |
| RF-06 | El administrador puede eliminar un usuario cliente únicamente si ese usuario no tiene reservas pendientes. | Alta |
| RF-07 | La página principal muestra un catálogo de barcos organizado por categorías, con campos de nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día. | Alta |
| RF-08 | El cliente puede buscar barcos por nombre o título desde la página de inicio. | Alta |
| RF-09 | El cliente puede aplicar filtros combinables de puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma simultánea e independiente. | Alta |
| RF-10 | Los filtros de puerto y fabricante se presentan como desplegables con valores válidos. | Alta |
| RF-11 | El filtro de fechas muestra todos los barcos del catálogo, marcando con una etiqueta 'No disponible' los que no están disponibles en ese rango sin ocultarlos. | Alta |
| RF-12 | Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo. | Alta |
| RF-13 | El cliente puede acceder a la ficha del barco desde el catálogo, visualizando los datos del barco y su imagen. | Alta |
| RF-14 | Desde la ficha de barco, el cliente puede seleccionar la cantidad de unidades disponibles y añadir a la cesta. | Alta |
| RF-15 | El administrador dispone de una ficha de barco propia con acciones de gestión: alta, edición y baja. | Alta |
| RF-16 | La cesta está siempre visible desde cualquier página de la aplicación. | Alta |
| RF-17 | El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta. | Alta |
| RF-18 | El usuario puede revisar el estado de la cesta desde el catálogo. | Alta |
| RF-19 | Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro. | Alta |
| RF-20 | Desde la cesta el usuario puede finalizar la compra iniciando el proceso de reserva. | Alta |
| RF-21 | El proceso de reserva se realiza en no más de tres pasos sin exigir registro previo. | Alta |
| RF-22 | Durante el proceso de reserva se solicitan los datos del cliente y los datos de pago, heredándose los datos si hay sesión iniciada. | Alta |
| RF-23 | El cliente puede pagar mediante PayPal Sandbox. | Alta |
| RF-24 | El cliente puede pagar mediante contra-reembolso. | Alta |
| RF-25 | Al finalizar la reserva, el cliente recibe un correo electrónico con los datos del barco, el rango de fechas, el importe total y un código de seguimiento. | Alta |
| RF-26 | Los alquileres se miden por día. | Alta |
| RF-27 | Se aplica una tasa de combustible de 50 euros por día, excepto para barcos de categoría velero donde la tasa es 0 euros. | Alta |
| RF-28 | Cada reserva tiene uno de los estados: PENDIENTE DE PAGO, PAGADO, EN USO o DEVUELTO. | Alta |
| RF-29 | Una reserva puede cancelarse únicamente si está en estado PENDIENTE DE PAGO, implicando su eliminación del sistema. | Alta |
| RF-30 | Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario. | Alta |
| RF-31 | El administrador puede cambiar el estado de una reserva desde el panel de reservas mediante botones por transición aplicable. | Alta |
| RF-32 | El cliente puede consultar el estado de su reserva usando el código de seguimiento recibido por email, incluso si no está registrado. | Alta |
| RF-33 | El usuario registrado puede consultar el estado de sus reservas desde su cuenta. | Alta |
| RF-34 | El administrador puede consultar el estado de cualquier reserva. | Alta |
| RF-35 | Existe un panel de administración propio de la aplicación para gestionar barcos, clientes y reservas. | Alta |
| RF-36 | El administrador puede realizar operaciones de alta, edición y baja de barcos desde el panel de administración. | Alta |
| RF-37 | El administrador puede consultar y eliminar clientes desde el panel de administración, respetando la restricción de no eliminar usuarios con reservas pendientes. | Alta |
| RF-38 | El administrador puede consultar y cambiar el estado de reservas desde el panel de administración. | Alta |

## Requisitos no funcionales

Total: **9**

| ID | Categoría | Condición / Métrica | Prioridad |
|---|---|---|---|
| RNF-01 | Lenguaje y Framework | La aplicación está desarrollada en Python usando Django 3.2. | Alta |
| RNF-02 | Base de Datos | La aplicación utiliza SQLite como base de datos. | Alta |
| RNF-03 | Pasarela de Pago | La integración de PayPal utiliza el entorno Sandbox, no producción. | Alta |
| RNF-04 | Empaquetado | La aplicación se entrega como contenedor Docker con Dockerfile incluido e instrucciones de construcción y arranque en README. | Alta |
| RNF-05 | Zona Horaria y Locale | La zona horaria configurada es Europe/Madrid y el locale es español. | Alta |
| RNF-06 | Idioma de Interfaz | La interfaz de usuario está íntegramente en español. | Alta |
| RNF-07 | Seguridad | Las contraseñas se almacenan usando el mecanismo estándar de Django, no en texto plano. CSRF está activo y se validan todos los formularios. | Alta |
| RNF-08 | Datos de Ejemplo | La aplicación arranca con datos precargados: mínimo 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (incluyendo velero), 1 usuario administrador de prueba y 1 usuario cliente de prueba. | Alta |
| RNF-09 | Idioma del Código | Los nombres de variables, clases, funciones y rutas están en inglés; comentarios y docstrings en español. | Media |
