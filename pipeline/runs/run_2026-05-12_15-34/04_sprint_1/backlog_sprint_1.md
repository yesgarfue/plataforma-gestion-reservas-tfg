---
run_id: run_2026-05-12_15-34
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-12T15:59:09+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Backlog del sprint

**ID de ejecución**: `run_2026-05-12_15-34`

Total de historias: **9**

## Historias del sprint

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme con correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Las contraseñas se almacenan de forma segura, no en texto plano.
- Se activa protección CSRF en el formulario de registro.

### HU-02 — Inicio de sesión de cliente

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error sin revelar qué campo es incorrecto.
- Se activa protección CSRF en el formulario de login.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para terminar mi sesión de forma segura.

**Criterios de aceptación**

- El cliente puede pulsar un botón 'Cerrar sesión' desde cualquier página.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se invalida completamente en el servidor.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver el catálogo de barcos organizado por categorías en la página principal, para explorar los barcos disponibles.

**Criterios de aceptación**

- La página principal muestra todos los barcos del catálogo.
- Los barcos se organizan por categorías.
- Los barcos no disponibles en un rango de fechas muestran una etiqueta 'No disponible'.
- El catálogo carga con los datos seed: 5 barcos, 2 puertos, 2 fabricantes, 2 categorías (una de ellas 'velero').

### HU-05 — Búsqueda de barcos por nombre

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero buscar barcos por nombre o título, para encontrar rápidamente el barco que me interesa.

**Criterios de aceptación**

- El cliente puede introducir un término de búsqueda en un campo de búsqueda.
- La búsqueda filtra el catálogo por nombre o título del barco.
- Si no hay resultados, se muestra un mensaje indicando que no se encontraron barcos.

### HU-06 — Filtros combinables del catálogo

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero aplicar filtros combinables (puertos, fabricantes, precio y cantidad) al catálogo, para refinar mi búsqueda de barcos.

**Criterios de aceptación**

- El cliente puede filtrar por puerto.
- El cliente puede filtrar por fabricante.
- El cliente puede filtrar por rango de precio.
- El cliente puede filtrar por cantidad disponible.
- Los filtros pueden aplicarse simultáneamente de forma independiente.
- El catálogo se actualiza en tiempo real al cambiar los filtros.

### HU-07 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la ficha detallada de un barco y seleccionar la cantidad de unidades que deseo reservar, para añadirlas a mi cesta.

**Criterios de aceptación**

- La ficha del barco muestra todos los detalles del barco (nombre, descripción, precio, categoría, fabricante, puerto).
- El cliente puede seleccionar la cantidad de unidades a reservar.
- El cliente puede añadir la cantidad seleccionada a su cesta.
- Se muestra un mensaje de confirmación tras añadir a la cesta.

### HU-21 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero operar bajo la zona horaria Europe/Madrid con locale español, para que todas las fechas y textos se muestren correctamente.

**Criterios de aceptación**

- La zona horaria del sistema está configurada como Europe/Madrid.
- El locale del sistema está configurado como español.
- Las fechas se muestran en formato español (DD/MM/YYYY).
- Los textos de la interfaz se muestran en español.

### HU-22 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como operador, quiero que la aplicación esté empaquetada en un contenedor Docker con instrucciones claras, para desplegar la aplicación de forma consistente.

**Criterios de aceptación**

- La aplicación incluye un Dockerfile con las instrucciones de construcción.
- El README contiene instrucciones claras para construir y arrancar el contenedor.
- El contenedor arranca correctamente con los datos seed precargados.
- La aplicación es accesible desde el contenedor en el puerto configurado.
