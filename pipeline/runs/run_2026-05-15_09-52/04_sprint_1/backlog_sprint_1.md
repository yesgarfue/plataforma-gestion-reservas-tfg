---
run_id: run_2026-05-15_09-52
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-15T10:00:43+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Backlog del sprint

**ID de ejecución**: `run_2026-05-15_09-52`

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
- El cliente puede filtrar por precio, categoría, capacidad y rango de fechas de forma independiente.
- Los filtros son combinables entre sí.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.
- El filtro de fechas muestra todos los barcos del catálogo marcando con etiqueta 'No disponible' aquellos no disponibles en ese rango, sin ocultarlos.

### HU-05 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero buscar barcos por nombre o título, para localizar rápidamente un barco específico.

**Criterios de aceptación**

- El cliente puede introducir un término de búsqueda en un campo de búsqueda.
- El sistema filtra los barcos del catálogo por nombre o título que coincidan con el término.
- La búsqueda es sensible a mayúsculas y minúsculas o realiza búsqueda insensible según implementación.

### HU-06 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha de un barco desde el catálogo, visualizar sus datos e imagen, y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede pulsar sobre un barco en el catálogo para acceder a su ficha.
- La ficha muestra todos los datos del barco e imagen.
- El cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco a la cesta desde la ficha.

### HU-20 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria en Europe/Madrid y el locale en español, para que la aplicación funcione con la zona horaria y el idioma correcto.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado en español.
- Las fechas y horas se muestran en la zona horaria correcta.
- La interfaz de usuario está íntegramente en español.

### HU-21 — Datos precargados de ejemplo

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero que la aplicación arranque con datos precargados de ejemplo, para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación arranca con mínimo 5 barcos precargados.
- Hay 2 puertos precargados.
- Hay 2 fabricantes precargados.
- Hay 2 categorías precargadas, incluyendo velero.
- Hay 1 usuario administrador de prueba precargado.
- Hay 1 usuario cliente de prueba precargado.
- Los datos se cargan de forma fiable en cada arranque.
