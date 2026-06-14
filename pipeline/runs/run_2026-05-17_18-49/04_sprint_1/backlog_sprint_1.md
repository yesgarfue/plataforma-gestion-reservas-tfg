---
run_id: run_2026-05-17_18-49
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-17T19:43:33+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Backlog del sprint

**ID de ejecución**: `run_2026-05-17_18-49`

Total de historias: **9**

## Historias del sprint

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme mediante correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Las contraseñas se almacenan usando el mecanismo estándar de Django, no en texto plano.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Se validan todos los formularios y está activa la protección CSRF.

### HU-02 — Inicio de sesión de cliente

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo electrónico y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error.
- Se valida el formulario y está activa la protección CSRF.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para terminar mi sesión de forma segura.

**Criterios de aceptación**

- El cliente puede acceder a una opción de cerrar sesión desde cualquier página.
- Al cerrar sesión, la sesión se termina y el cliente es redirigido a la página principal.
- Tras cerrar sesión, el cliente no puede acceder a funcionalidades autenticadas sin volver a iniciar sesión.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Los barcos se organizan por categorías.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.
- La interfaz está íntegramente en español.

### HU-05 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero buscar barcos por nombre o título desde la página de inicio, para encontrar rápidamente el barco que me interesa.

**Criterios de aceptación**

- El cliente puede introducir un término de búsqueda en un campo de búsqueda.
- La búsqueda filtra los barcos por nombre o título coincidentes.
- Los resultados se actualizan dinámicamente o tras enviar el formulario.

### HU-06 — Filtros combinables de catálogo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero aplicar filtros combinables de puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma simultánea e independiente, para refinar mi búsqueda.

**Criterios de aceptación**

- El cliente puede filtrar por puerto mediante un desplegable con valores válidos.
- El cliente puede filtrar por fabricante mediante un desplegable con valores válidos.
- El cliente puede filtrar por rango de precio.
- El cliente puede filtrar por categoría.
- El cliente puede filtrar por capacidad.
- El cliente puede filtrar por rango de fechas.
- Los filtros se aplican de forma combinada e independiente.
- Al filtrar por fechas, se muestran todos los barcos del catálogo, marcando con una etiqueta 'No disponible' los que no están disponibles en ese rango sin ocultarlos.

### HU-07 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha del barco desde el catálogo, visualizar sus datos e imagen, y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede hacer clic en un barco del catálogo para acceder a su ficha.
- La ficha muestra todos los datos del barco y su imagen.
- El cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta desde la ficha.
- Se valida que la cantidad seleccionada no exceda la disponibilidad.

### HU-21 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria en Europe/Madrid y el locale en español para que todas las fechas y textos se muestren correctamente.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado en español.
- Todas las fechas se muestran en la zona horaria Europe/Madrid.
- La interfaz de usuario está íntegramente en español.
- Los nombres de variables, clases, funciones y rutas están en inglés; comentarios y docstrings en español.

### HU-22 — Datos precargados de ejemplo

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero que la aplicación arranque con datos precargados para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación arranca con mínimo 5 barcos precargados.
- Hay 2 puertos precargados.
- Hay 2 fabricantes precargados.
- Hay 2 categorías precargadas, incluyendo velero.
- Hay 1 usuario administrador de prueba precargado.
- Hay 1 usuario cliente de prueba precargado.
- Los datos se cargan de forma fiable en cada arranque.
