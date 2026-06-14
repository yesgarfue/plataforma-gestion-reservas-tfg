---
run_id: run_2026-05-14_11-32
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-14T11:57:01+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Backlog del sprint

**ID de ejecución**: `run_2026-05-14_11-32`

Total de historias: **8**

## Historias del sprint

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme con correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Las contraseñas se almacenan usando el mecanismo estándar de Django, no en texto plano.
- Tras registrarse, el cliente queda autenticado en la sesión.
- El formulario incluye validación CSRF.

### HU-02 — Inicio de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error.
- El formulario incluye validación CSRF.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para salir de mi cuenta de forma segura.

**Criterios de aceptación**

- El cliente puede pulsar un botón de cierre de sesión desde cualquier página.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se elimina del servidor.

### HU-04 — Catálogo de barcos con filtros combinables

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero visualizar un catálogo de barcos organizado por categorías y filtrar por puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma combinable, para encontrar el barco que necesito.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- El filtro de fechas muestra todos los barcos del catálogo, marcando con etiqueta 'No disponible' aquellos no disponibles en ese rango sin ocultarlos.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.
- Los filtros funcionan de forma combinable e independiente.
- El sistema permite búsqueda de barcos por nombre o título desde la página de inicio.

### HU-05 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha de barco desde el catálogo y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede acceder a la ficha de barco desde el catálogo.
- La ficha muestra los datos del barco e imagen.
- Desde la ficha, el cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta con la cantidad seleccionada.

### HU-06 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero visualizar, modificar y vaciar mi cesta desde cualquier página de la aplicación, para gestionar mis barcos antes de reservar.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta completamente.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.

### HU-16 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria en Europe/Madrid y el locale en español para que la aplicación funcione correctamente en el contexto regional.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado en español.
- La interfaz de usuario está íntegramente en español.
- Los nombres de variables, clases, funciones y rutas están en inglés; comentarios y docstrings en español.

### HU-17 — Datos precargados y Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero arrancar con datos precargados y estar empaquetado en Docker para facilitar el despliegue y las pruebas.

**Criterios de aceptación**

- La aplicación arranca con datos precargados: mínimo 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (incluyendo velero), 1 usuario administrador de prueba y 1 usuario cliente de prueba.
- La aplicación se entrega como contenedor Docker con Dockerfile incluido.
- Se incluyen instrucciones de construcción y arranque en README.
- La aplicación está desarrollada en Python usando Django 3.2.
- La aplicación utiliza SQLite como base de datos.
