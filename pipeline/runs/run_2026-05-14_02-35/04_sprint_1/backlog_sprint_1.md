---
run_id: run_2026-05-14_02-35
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-14T02:48:23+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Backlog del sprint

**ID de ejecución**: `run_2026-05-14_02-35`

Total de historias: **10**

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

Como cliente, quiero ver un catálogo de barcos organizado por categorías y aplicar filtros combinables de puertos, fabricantes, precio, categoría, capacidad y rango de fechas, para encontrar el barco que necesito.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos con campos de nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- El cliente puede buscar barcos por nombre o título desde la página de inicio.
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos.
- El cliente puede aplicar filtros de puertos, fabricantes, precio, categoría, capacidad y rango de fechas de forma simultánea e independiente.
- El filtro de fechas muestra todos los barcos del catálogo, marcando con una etiqueta 'No disponible' aquellos no disponibles en ese rango sin ocultarlos.
- Los barcos agotados o no disponibles aparecen claramente marcados en el catálogo.

### HU-05 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero acceder a la ficha de un barco desde el catálogo y seleccionar la cantidad de unidades disponibles para añadir a la cesta.

**Criterios de aceptación**

- El cliente puede acceder a la ficha del barco desde el catálogo.
- La ficha visualiza los datos del barco y su imagen.
- Desde la ficha de barco, el cliente puede seleccionar la cantidad de unidades disponibles.
- El cliente puede añadir el barco seleccionado a la cesta.
- Se valida que la cantidad seleccionada no exceda la disponibilidad.

### HU-06 — Gestión de cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la cesta siempre visible, modificar las cantidades de barcos y revisar el estado de la cesta desde el catálogo.

**Criterios de aceptación**

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- El usuario puede vaciar la cesta completamente.
- Al entrar en modo administrador, la cesta se vacía y el administrador no puede añadir barcos al carro.

### HU-20 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero configurar la zona horaria a Europe/Madrid y el locale a español para que la aplicación funcione en el contexto correcto.

**Criterios de aceptación**

- La zona horaria configurada es Europe/Madrid.
- El locale está configurado como español.
- Todas las fechas y horas se muestran en la zona horaria Europe/Madrid.
- Los formatos de fecha y número siguen la convención española.

### HU-21 — Interfaz de usuario en español

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como usuario, quiero que la interfaz de usuario esté íntegramente en español, para una mejor comprensión y usabilidad.

**Criterios de aceptación**

- Todos los textos de la interfaz están en español.
- Los mensajes de error están en español.
- Los botones, etiquetas y campos están en español.
- Los correos electrónicos están en español.

### HU-22 — Datos precargados en arranque

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como desarrollador, quiero que la aplicación arranque con datos de ejemplo precargados para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación arranca con mínimo 5 barcos precargados.
- Hay 2 puertos precargados.
- Hay 2 fabricantes precargados.
- Hay 2 categorías precargadas, incluyendo velero.
- Hay 1 usuario administrador de prueba precargado.
- Hay 1 usuario cliente de prueba precargado.
- Los datos se cargan automáticamente en cada arranque del contenedor.

### HU-23 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como operador, quiero que la aplicación se entregue como contenedor Docker con instrucciones claras de construcción y arranque.

**Criterios de aceptación**

- La aplicación incluye un Dockerfile.
- El Dockerfile contiene instrucciones para construir la imagen.
- Se incluye un README con instrucciones de construcción del contenedor.
- Se incluye un README con instrucciones de arranque del contenedor.
- El contenedor arranca correctamente con los datos precargados.
