---
run_id: run_2026-05-12_16-48
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-12T17:03:51+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Backlog del sprint

**ID de ejecución**: `run_2026-05-12_16-48`

Total de historias: **10**

## Historias del sprint

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme mediante correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Las contraseñas se almacenan de forma segura, no en texto plano.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Se valida que el correo no esté ya registrado.

### HU-02 — Inicio de sesión

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error.
- El cliente puede iniciar sesión durante el proceso de reserva, reconstruyendo la cesta.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para salir de mi cuenta de forma segura.

**Criterios de aceptación**

- El cliente puede hacer clic en un botón de cierre de sesión.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se termina en el servidor.

### HU-05 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos.
- Los barcos están organizados por categorías.
- Cada barco muestra nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- Los barcos agotados o no disponibles aparecen claramente marcados.

### HU-06 — Búsqueda y filtros combinables

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero buscar barcos por nombre y aplicar filtros combinables, para encontrar la embarcación que se ajuste a mis necesidades.

**Criterios de aceptación**

- Se puede buscar por nombre o título de barco.
- Los filtros combinables incluyen puertos, fabricantes, precio, categoría, capacidad y rango de fechas.
- Los filtros por puerto y fabricante se presentan como desplegables con valores válidos.
- Los filtros se aplican de forma combinada.
- Los resultados se actualizan al aplicar o cambiar filtros.

### HU-07 — Ficha de barco y selección de cantidad

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver la ficha detallada de un barco y seleccionar la cantidad de unidades, para añadirlo a mi cesta.

**Criterios de aceptación**

- La ficha del barco muestra todos los datos del barco e imagen.
- El cliente puede seleccionar la cantidad de unidades del barco.
- El cliente puede añadir el barco a la cesta desde la ficha.
- Se valida que la cantidad sea mayor a cero.

### HU-21 — Configuración de locale y zona horaria

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero operar con la zona horaria Europe/Madrid y localización española, para que todas las fechas y textos sean correctos para el usuario.

**Criterios de aceptación**

- La aplicación está configurada con zona horaria Europe/Madrid.
- La interfaz de usuario está íntegramente en español.
- Las fechas se muestran en formato español.
- Los textos del sistema están en español.

### HU-22 — Seguridad de contraseñas y CSRF

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero aplicar medidas de seguridad básicas para proteger las contraseñas y prevenir ataques CSRF.

**Criterios de aceptación**

- Las contraseñas no se almacenan en texto plano.
- Se aplica CSRF activo en todos los formularios.
- Las contraseñas se validan según estándares de seguridad de Django.

### HU-23 — Datos seed precargados

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como sistema, quiero que la aplicación arranque con datos pre-cargados, para poder probar todas las funcionalidades de manera automática.

**Criterios de aceptación**

- La aplicación incluye un script de carga de datos iniciales.
- Los datos seed incluyen barcos de diferentes categorías, puertos y fabricantes.
- Los datos seed incluyen clientes de prueba.
- Los datos seed incluyen reservas en diferentes estados.
- Los datos se cargan automáticamente al iniciar la aplicación.

### HU-24 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como equipo de desarrollo, quiero que la aplicación se empaquete en un contenedor Docker, para facilitar el despliegue y la reproducibilidad del entorno.

**Criterios de aceptación**

- La aplicación incluye un Dockerfile funcional.
- El contenedor incluye todas las dependencias necesarias.
- Se proporciona un README con instrucciones de construcción y ejecución del contenedor.
- El contenedor se puede ejecutar sin configuración adicional.
