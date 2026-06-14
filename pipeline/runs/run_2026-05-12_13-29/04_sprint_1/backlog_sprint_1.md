---
run_id: run_2026-05-12_13-29
fase: 04_sprint_1
agente: Script
modelo: deterministico
timestamp: 2026-05-12T13:56:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# Sprint 1 — Backlog del sprint

**ID de ejecución**: `run_2026-05-12_13-29`

Total de historias: **11**

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
- El sistema valida que el correo no esté ya registrado.

### HU-02 — Inicio de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente registrado, quiero iniciar sesión con correo y contraseña, para acceder a las funcionalidades reservadas a usuarios autenticados.

**Criterios de aceptación**

- El formulario de login acepta correo y contraseña.
- Tras un login correcto, el cliente accede a su cuenta.
- Tras un login incorrecto, se muestra un mensaje de error sin revelar qué campo es incorrecto.
- La sesión se mantiene activa durante la navegación.

### HU-03 — Cierre de sesión

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente autenticado, quiero cerrar sesión explícitamente, para asegurar que mi cuenta no permanece abierta en dispositivos compartidos.

**Criterios de aceptación**

- El cliente puede hacer clic en un botón 'Cerrar sesión' desde cualquier página.
- Al cerrar sesión, la cesta se mantiene pero el cliente queda desautenticado.
- Tras cerrar sesión, el cliente es redirigido a la página principal.

### HU-04 — Catálogo de barcos por categorías

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero ver un catálogo de barcos organizado por categorías en la página principal, para explorar las opciones disponibles.

**Criterios de aceptación**

- La página principal muestra un catálogo de barcos.
- Los barcos están organizados por categorías.
- Cada barco muestra nombre, imagen obligatoria, categoría, fabricante, puerto, capacidad y precio por día.
- Los barcos agotados o no disponibles están claramente marcados.

### HU-05 — Búsqueda y filtros combinables de barcos

- **Prioridad**: Alta
- **Estimación**: L

**Descripción**

Como cliente, quiero buscar barcos por nombre y aplicar filtros combinables, para encontrar rápidamente el barco que necesito.

**Criterios de aceptación**

- La búsqueda está disponible en la página de inicio.
- La búsqueda acepta búsquedas por nombre o título del barco.
- Se pueden aplicar filtros combinables (puerto, fabricante, categoría, capacidad, precio, fechas).
- Los resultados se actualizan al aplicar o cambiar filtros.
- La búsqueda devuelve resultados relevantes o un mensaje si no hay coincidencias.

### HU-06 — Selección de cantidad y adición a cesta

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como cliente, quiero seleccionar la cantidad de unidades de un barco desde su ficha y añadirlo a la cesta, para preparar mi reserva.

**Criterios de aceptación**

- La ficha del barco permite seleccionar una cantidad de unidades.
- El cliente puede añadir el barco a la cesta desde la ficha.
- La cesta se actualiza inmediatamente tras añadir el barco.
- Se valida que la cantidad sea mayor a cero.

### HU-07 — Visibilidad permanente de la cesta

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como cliente, quiero que la cesta esté siempre visible desde cualquier página de la aplicación, para saber en todo momento qué he añadido.

**Criterios de aceptación**

- La cesta es visible en todas las páginas de la aplicación.
- La cesta muestra el número de unidades totales.
- La cesta muestra el importe total.
- El cliente puede acceder a la cesta desde cualquier página.

### HU-22 — Configuración de zona horaria y locale

- **Prioridad**: Alta
- **Estimación**: S

**Descripción**

Como administrador del sistema, quiero que la aplicación funcione bajo la zona horaria Europe/Madrid y locale español, para que las fechas y textos sean correctos para los usuarios.

**Criterios de aceptación**

- La zona horaria del sistema está configurada como Europe/Madrid.
- El locale está configurado como español.
- Las fechas se muestran en formato español.
- Los textos de la interfaz están en español.
- Los correos electrónicos se envían con la zona horaria correcta.

### HU-23 — Datos seed precargados

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador, quiero que la aplicación arranque con datos precargados, para poder demostrar la funcionalidad sin necesidad de crear datos manualmente.

**Criterios de aceptación**

- La aplicación carga 5 barcos al iniciar.
- La aplicación carga 2 puertos al iniciar.
- La aplicación carga 2 fabricantes al iniciar.
- La aplicación carga 2 categorías al iniciar.
- La aplicación carga 1 usuario administrador al iniciar.
- La aplicación carga 1 cliente de prueba al iniciar.
- Los datos se cargan de forma fiable en cada arranque.

### HU-24 — Empaquetado en Docker

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como operador, quiero que la aplicación sea entregada como contenedor Docker, para facilitar el despliegue y la ejecución en diferentes entornos.

**Criterios de aceptación**

- Existe un Dockerfile que construye la imagen de la aplicación.
- El Dockerfile incluye todas las dependencias necesarias.
- Existe un README con instrucciones de construcción del contenedor.
- Existe un README con instrucciones de arranque del contenedor.
- El contenedor arranca correctamente y la aplicación es accesible.

### HU-25 — Seguridad: contraseñas, CSRF y validación

- **Prioridad**: Alta
- **Estimación**: M

**Descripción**

Como administrador de seguridad, quiero que la aplicación implemente medidas de seguridad mínima, para proteger los datos de los usuarios.

**Criterios de aceptación**

- Las contraseñas no se almacenan en texto plano.
- La protección CSRF está activa en todos los formularios.
- Se validan todos los formularios en el servidor.
- Se validan los datos de entrada para prevenir inyecciones.
- Los errores no revelan información sensible al usuario.
