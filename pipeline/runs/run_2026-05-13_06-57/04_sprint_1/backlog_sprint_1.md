---
run_id: run_2026-05-13_06-57
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-13T07:11:55+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Backlog del sprint

**ID de ejecución**: `run_2026-05-13_06-57`

Total de historias: **10**

## Historias del sprint

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme con correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Las contraseñas se almacenan de forma segura utilizando el mecanismo estándar de Django.

### HU-02 — Inicio de sesión de cliente

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error.
- La protección CSRF está activada en el formulario.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para terminar mi sesión de forma segura.

**Criterios de aceptación**

- El cliente puede hacer clic en un botón 'Cerrar sesión'.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se elimina del servidor.

### HU-05 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver el catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal presenta los barcos agrupados por categoría.
- Cada categoría es claramente identificable.
- Se muestran al menos 5 barcos predefinidos en el catálogo.

### HU-06 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente, quiero buscar barcos por nombre o título en la página de inicio, para encontrar rápidamente el barco que me interesa.

**Criterios de aceptación**

- Existe un campo de búsqueda en la página principal.
- La búsqueda filtra los barcos por nombre o título.
- Los resultados se actualizan en tiempo real o tras enviar el formulario.

### HU-07 — Filtros combinables de catálogo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero filtrar el catálogo por puertos, fabricantes, precio, categoría, capacidad y rango de fechas, para encontrar el barco que se ajuste a mis necesidades.

**Criterios de aceptación**

- Los filtros de puertos y fabricante se presentan como desplegables con valores válidos.
- El cliente puede combinar múltiples filtros simultáneamente.
- Los barcos no disponibles en el rango de fechas seleccionado aparecen marcados con una etiqueta 'No disponible'.
- Los filtros se aplican correctamente al catálogo.

### HU-08 — Ficha de barco con selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha detallada de un barco e indicar la cantidad que deseo alquilar, para añadirlo a la cesta.

**Criterios de aceptación**

- La ficha del barco muestra todos los detalles relevantes (nombre, descripción, precio, categoría, capacidad, puerto, fabricante).
- El cliente puede seleccionar la cantidad de unidades a alquilar.
- El cliente puede añadir el barco a la cesta desde la ficha.

### HU-22 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero operar bajo la zona horaria 'Europe/Madrid' y presentar la interfaz íntegramente en español, para garantizar consistencia regional.

**Criterios de aceptación**

- La zona horaria del sistema está configurada como 'Europe/Madrid'.
- Todos los textos de la interfaz están en español.
- Las fechas y horas se muestran en formato español.
- Los mensajes de error y validación están en español.

### HU-23 — Empaquetado Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como equipo de desarrollo, quiero que la aplicación se empaquete y ejecute como contenedor Docker, para facilitar el despliegue y la consistencia del entorno.

**Criterios de aceptación**

- Existe un Dockerfile que define la imagen de la aplicación.
- La aplicación se ejecuta correctamente dentro del contenedor Docker.
- El contenedor incluye todas las dependencias necesarias (Python, Django, SQLite).
- El contenedor se puede construir y ejecutar sin errores.

### HU-24 — Datos seed iniciales

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero arrancar con datos predefinidos (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, 1 usuario administrador y cliente), para que la aplicación sea funcional desde el inicio.

**Criterios de aceptación**

- La aplicación carga automáticamente 5 barcos al arrancar.
- Se crean 2 puertos predefinidos.
- Se crean 2 fabricantes predefinidos.
- Se crean 2 categorías predefinidas.
- Se crea 1 usuario administrador con credenciales de prueba.
- Se crea 1 usuario cliente con credenciales de prueba.
- Los datos seed se cargan de forma fiable en cada arranque.
