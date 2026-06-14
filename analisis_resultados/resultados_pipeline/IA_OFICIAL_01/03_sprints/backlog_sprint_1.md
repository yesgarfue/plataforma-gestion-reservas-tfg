---
run_id: run_2026-05-18_15-09
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-18T16:03:30+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Backlog del sprint

**ID de ejecución**: `run_2026-05-18_15-09`

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

Como cliente autenticado, quiero cerrar sesión explícitamente, para terminar mi sesión de forma segura.

**Criterios de aceptación**

- El cliente puede acceder a una opción de cerrar sesión desde cualquier página.
- Al cerrar sesión, la sesión se invalida y el cliente es redirigido a la página principal.
- Tras cerrar sesión, el cliente no puede acceder a funcionalidades autenticadas sin volver a iniciar sesión.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías en la página principal, para explorar las embarcaciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Los barcos se organizan por categorías.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.
- La interfaz está íntegramente en español.

### HU-05 — Búsqueda y filtrado de barcos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero buscar barcos por nombre y filtrar por puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma combinable, para encontrar el barco que necesito.

**Criterios de aceptación**

- El sistema permite buscar barcos por nombre o título desde la página de inicio.
- El sistema permite filtrar barcos por puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma combinable e independiente.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- El filtro de fechas muestra todos los barcos del catálogo, marcando con una etiqueta 'No disponible' aquellos no disponibles en ese rango sin ocultarlos.
- Los barcos no disponibles en el rango de fechas seleccionado aparecen claramente marcados.

### HU-06 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha del barco desde el catálogo y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede acceder a la ficha del barco desde el catálogo.
- La ficha visualiza los datos del barco e imagen.
- Desde la ficha de barco, el cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco seleccionado a la cesta.
- Si el barco está agotado, no se permite añadir a la cesta.

### HU-20 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria en Europe/Madrid y el locale en español para asegurar que las fechas y textos se muestren correctamente.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado en español.
- Las fechas se muestran en formato español.
- Los textos del sistema están en español.

### HU-21 — Datos precargados de ejemplo

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero arrancar con datos precargados para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación arranca con mínimo 5 barcos precargados.
- Hay mínimo 2 puertos precargados.
- Hay mínimo 2 fabricantes precargados.
- Hay mínimo 2 categorías precargadas, incluyendo velero.
- Hay 1 usuario administrador de prueba precargado.
- Hay 1 usuario cliente de prueba precargado.
