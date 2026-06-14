---
run_id: run_2026-05-13_15-33
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-13T15:53:10+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Backlog del sprint

**ID de ejecución**: `run_2026-05-13_15-33`

Total de historias: **9**

## Historias del sprint

### HU-01 — Registro de cliente

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como visitante, quiero registrarme con correo electrónico y contraseña, para poder acceder a mi cuenta y consultar mis reservas.

**Criterios de aceptación**

- El formulario de registro acepta correo electrónico y contraseña.
- Las contraseñas se almacenan de forma segura, no en texto plano.
- Tras registrarse, el cliente queda autenticado en la sesión.
- Se valida que el correo no esté ya registrado.

### HU-02 — Inicio de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error genérico.
- La sesión se mantiene activa durante la navegación.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para asegurar que mi cuenta no queda accesible desde el dispositivo.

**Criterios de aceptación**

- El cliente puede hacer clic en un botón 'Cerrar sesión'.
- Tras cerrar sesión, el cliente es redirigido a la página principal.
- La sesión se invalida y el cliente no puede acceder a funcionalidades autenticadas sin volver a iniciar sesión.

### HU-05 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver el catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos.
- Los barcos están organizados por categorías.
- Cada barco muestra: nombre, imagen, categoría, fabricante, puerto, capacidad y precio por día.
- El catálogo es accesible sin necesidad de autenticación.

### HU-06 — Búsqueda y filtros combinables de barcos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero buscar y filtrar barcos por nombre, puertos, fabricantes, precio, categoría, capacidad y fechas, para encontrar la embarcación que se ajuste a mis necesidades.

**Criterios de aceptación**

- La búsqueda funciona por nombre o título del barco.
- Los filtros de puertos, fabricante y precio se presentan como desplegables.
- Los filtros de categoría y capacidad están disponibles.
- El filtro de fechas muestra todos los barcos del catálogo; los no disponibles en ese rango aparecen marcados con una etiqueta 'No disponible'.
- Los filtros son combinables entre sí.
- Los resultados se actualizan al aplicar o modificar filtros.

### HU-22 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como sistema, quiero operar con zona horaria Europe/Madrid y locale español, para que todas las fechas, horas y textos se muestren correctamente.

**Criterios de aceptación**

- La aplicación está configurada con zona horaria Europe/Madrid.
- La aplicación utiliza locale español.
- Las fechas y horas se muestran en formato español.
- Los textos de la interfaz están en español.

### HU-23 — Datos seed precargados

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como desarrollador, quiero que la aplicación arranque con datos precargados que permitan probar todas las funcionalidades sin trabajo previo, para facilitar las pruebas y demostraciones.

**Criterios de aceptación**

- La aplicación incluye un conjunto de barcos de ejemplo en diferentes categorías.
- La aplicación incluye clientes de ejemplo.
- La aplicación incluye reservas de ejemplo en diferentes estados.
- Los datos seed se cargan automáticamente al iniciar la aplicación.
- Los datos seed permiten probar todos los filtros y funcionalidades.

### HU-24 — Seguridad: contraseñas, CSRF y validación

- **Prioridad**: Media
- **Estimación**: M

**Descripción**

Como sistema, quiero implementar medidas de seguridad mínima para proteger los datos de los usuarios.

**Criterios de aceptación**

- Las contraseñas no se almacenan en texto plano.
- La protección CSRF está activa en todos los formularios.
- Se validan todos los formularios en el servidor.
- Se validan los datos de entrada para prevenir inyecciones.
- Los errores de validación se muestran al usuario sin revelar información sensible.

### HU-25 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como operador, quiero que la aplicación esté empaquetada como contenedor Docker con instrucciones claras de construcción y arranque, para facilitar el despliegue.

**Criterios de aceptación**

- Existe un Dockerfile que define la construcción de la imagen.
- Existe un README con instrucciones de construcción del contenedor.
- Existe un README con instrucciones de arranque del contenedor.
- El contenedor incluye todas las dependencias necesarias.
- La aplicación funciona correctamente al ejecutarse desde el contenedor.
