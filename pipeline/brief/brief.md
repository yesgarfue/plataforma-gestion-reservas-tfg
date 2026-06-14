---
documento: brief
proyecto: Hundidos - Sistema de Alquiler de Barcos
version: 1.0
estado: congelado
fecha_creacion: 2026-04-24
fecha_congelacion: 2026-04-24
autor: Yesica Garate Fuentes
caso: caso02_pipeline_IA
---

# Brief del proyecto Hundidos

Este documento fija el alcance funcional y técnico del producto a desarrollar por el pipeline híbrido humano–IA del Caso 02. Una vez congelado, no se modifica durante la ejecución medida del pipeline. Cualquier ambigüedad detectada por los agentes se resuelve mediante regeneración con observaciones del gate humano, no mediante edición del brief.

El brief es la **única entrada** del pipeline. Los agentes no tienen acceso a otros documentos del proyecto baseline.

---

## 1. Identidad del proyecto

- **Nombre del producto**: Hundidos.
- **Tipo**: aplicación web de alquiler de embarcaciones de recreo (barcos y yates).
- **Contexto**: proyecto académico de la asignatura de Planificación y Gestión de Proyectos Informáticos. El pipeline IA debe producir un producto funcionalmente equivalente al desarrollado por el equipo humano baseline (Grupo G3.2), bajo las mismas restricciones técnicas y criterios de aceptación.
- **Marca**: el sitio se identifica como "Hundidos". Debe aparecer como nombre/logo textual en la cabecera del sitio. No se requiere diseño gráfico elaborado ni branding corporativo avanzado.
- **Idioma de la interfaz**: español.
- **Idioma del código**: nombres de variables, clases, funciones y rutas en inglés; comentarios y docstrings en español.

---

## 2. Objetivo funcional

Proveer una solución software funcional en la que un usuario pueda experimentar una experiencia de alquiler completa de una embarcación: navegar el catálogo, filtrar por distintos criterios, reservar para un rango de fechas, pagar (o dejar pendiente de pago), recibir confirmación por email y consultar el estado del alquiler. La aplicación debe permitir también la gestión administrativa del catálogo, usuarios y reservas.

---

## 3. Alcance funcional (obligatorio)

El producto **debe** implementar las funcionalidades siguientes. Son criterio de aceptación: si falta alguna, el producto no cumple el brief.

### 3.1. Usuarios, registro y sesión

- Dos roles diferenciados: **cliente** y **administrador**.
- Registro de cliente mediante correo electrónico y contraseña.
- Inicio de sesión con correo y contraseña.
- Cierre de sesión explícito.
- El registro permanente es **opcional** para el cliente: debe ser posible completar una reserva sin haberse registrado (el sistema recogerá los datos mínimos necesarios durante el proceso de reserva).
- El inicio de sesión puede realizarse **durante el proceso de reserva**: si el usuario tiene una cesta con barcos y decide iniciar sesión, al volver de la página de login debe recuperar la cesta y continuar el proceso.
- Un administrador puede eliminar un usuario cliente **únicamente si ese usuario no tiene reservas pendientes**.

### 3.2. Catálogo y búsqueda

- Página principal con catálogo de barcos organizado por categorías.
- Cada barco tiene los campos: nombre, imagen (una imagen obligatoria por barco), categoría, fabricante, puerto, capacidad, precio por día.
- Búsqueda disponible en la página de inicio.
- Búsqueda por nombre o título del barco.
- Filtros combinables: **puertos**, **fabricantes**, **precio**, **categoría**, **capacidad** y **rango de fechas**. Los tres primeros (puertos, fabricantes, precio) deben poder aplicarse **simultáneamente** y de forma independiente (no debe forzarse un orden entre ellos).
- Los filtros de puerto y fabricante se presentan como desplegables con valores válidos; no como campos de texto libre.
- El filtro de fechas muestra todos los barcos del catálogo: los no disponibles en ese rango aparecen marcados con una etiqueta "No disponible", sin ocultarse.
- Los barcos agotados o no disponibles aparecen claramente marcados.

### 3.3. Ficha de barco

- Ficha del barco accesible desde el catálogo, con los datos del barco y la imagen.
- Desde la ficha, el cliente puede seleccionar la **cantidad** de unidades del barco (si hay varias unidades disponibles) y añadir a la cesta.
- El administrador dispone de su propia ficha de barco con acciones de gestión (alta, edición, baja).

### 3.4. Cesta

- La cesta está siempre visible desde cualquier página de la aplicación.
- El usuario puede ampliar o reducir la cantidad de unidades de cada barco en la cesta.
- El usuario puede revisar el estado de la cesta desde el catálogo.
- **Al entrar en modo administrador, la cesta se vacía** y el administrador no puede añadir al carro.
- Desde la cesta el usuario puede finalizar la compra (proceso de reserva).

### 3.5. Proceso de reserva y pago

- La compra se realiza en no más de tres pasos, sin exigir registro previo.
- Durante el proceso se solicitan los datos del cliente (directamente o heredados si hay sesión iniciada) y los datos de pago.
- Dos métodos de pago disponibles:
  - **PayPal Sandbox** (entorno de pruebas de PayPal).
  - **Contra-reembolso**.
- Al finalizar, el cliente recibe un **correo electrónico** con: los datos del barco reservado, el rango de fechas, el importe total y un **código de seguimiento** del alquiler.
- Los alquileres se miden por día.
- Se aplica una **tasa de combustible de 50 € por día**, salvo que el barco sea de categoría "velero", en cuyo caso la tasa es 0 €.

### 3.6. Estados de reserva y cancelación

- Cada reserva tiene uno de los estados: **PENDIENTE DE PAGO**, **PAGADO**, **EN USO**, **DEVUELTO**. No existe un estado CANCELADO.
- Una reserva puede cancelarse **únicamente si está en estado PENDIENTE DE PAGO**. Cancelar una reserva implica su eliminación del sistema; no queda registrada con un estado posterior. No se contempla mecanismo de devolución para reservas ya pagadas.
- Si falta un día para el inicio de la reserva y sigue en estado PENDIENTE DE PAGO, el sistema envía un correo de recordatorio al usuario.
- El administrador puede cambiar el estado de una reserva desde el panel de reservas (un botón por transición aplicable).

### 3.7. Seguimiento de pedidos

- El cliente puede consultar el estado de su reserva usando el **código de seguimiento** recibido por email, incluso si no está registrado.
- El usuario registrado puede consultar el estado de sus reservas desde su cuenta.
- El administrador puede consultar el estado de cualquier reserva.

### 3.8. Gestión administrativa

- Panel de administración propio de la aplicación (no necesariamente el admin de Django por defecto).
- Gestión de barcos (alta, edición, baja).
- Gestión de clientes (consulta, eliminación con la restricción del 3.1).
- Gestión de reservas (consulta, cambio de estado).

---

## 4. Restricciones técnicas (obligatorias)

- **Lenguaje**: Python.
- **Framework web**: Django 3.2.
- **Base de datos**: SQLite.
- **Pasarela de pago**: PayPal Sandbox (no producción).
- **Empaquetado**: la aplicación debe entregarse como **contenedor Docker**, con instrucciones de construcción y arranque incluidas en un README.
- **Zona horaria y locale**: España (Europe/Madrid), español.
- **Seguridad mínima**: contraseñas no almacenadas en texto plano (se usa el mecanismo estándar de Django); CSRF activo; validación de formularios.
- **Datos de ejemplo (seed)**: la aplicación debe arrancar con datos precargados que permitan probar todas las funcionalidades sin trabajo previo del usuario. Como mínimo:
  - 5 barcos.
  - 2 puertos.
  - 2 fabricantes.
  - 2 categorías (una de ellas "velero", por la regla de la tasa de combustible).
  - 1 usuario administrador de prueba.
  - 1 usuario cliente de prueba.

---

## 5. Fuera de alcance

Los siguientes elementos **no forman parte** del producto a entregar y no deben ser implementados por el pipeline:

- Despliegue en PaaS (Render, Heroku, Railway u otros). El entregable es el contenedor Docker local; si el pipeline genera algún artefacto orientado a PaaS, se considera fuera de alcance y no puntúa.
- Pasarela de pago real (solo Sandbox).
- Aplicación móvil nativa.
- Integración con sistemas externos de reserva, CRM o ERP.
- Múltiples imágenes por barco (una imagen es el mínimo obligatorio; más de una queda como mejora opcional no requerida).
- Fianza parcial o abono del 20 % anticipado (rechazado por el patrocinador en el baseline, no forma parte del alcance).
- Devolución/reembolso para reservas en estado PAGADO (ver 3.6).
- Traducción a idiomas distintos del español.
- Gestión de múltiples tiendas, sedes o inquilinos.
- Sistema de valoraciones, reseñas o comentarios de clientes sobre los barcos.
- Recomendaciones personalizadas, motor de sugerencias o analytics.

---

## 6. Criterios mínimos de aceptación

El producto se evalúa en tres niveles. El resultado se reporta por niveles, de modo que un fallo en un nivel no invalida la medición de los demás. Solo un fallo en el Nivel A impide evaluar el resto.

### Nivel A — Arranque técnico mínimo (condición necesaria para evaluar funcionalidad)

- **A1**. La aplicación Django arranca localmente sin errores (`python manage.py runserver` o equivalente).
- **A2**. Los datos de ejemplo descritos en la sección 4 están precargados automáticamente al arranque, o existe un comando de gestión (`manage.py`) documentado en el README que los carga.
- **A3**. La aplicación es accesible desde el navegador en la URL documentada.

Si falla A1, A2 o A3, no es posible evaluar los niveles B y C, y el Run se reporta como "bloqueado en arranque". Este resultado es en sí mismo un dato del experimento, no un fallo del protocolo.

### Nivel B — Cumplimiento funcional (qué hace la aplicación)

Se evalúa el cumplimiento de cada bloque del alcance funcional de la sección 3:

- **B1**. Usuarios, registro y sesión (3.1).
- **B2**. Catálogo y búsqueda, incluyendo filtros combinables (3.2).
- **B3**. Ficha de barco con selección de cantidad (3.3).
- **B4**. Cesta siempre visible, modificable y vaciable al entrar como admin (3.4).
- **B5**. Proceso de reserva en no más de tres pasos, sin exigir registro (3.5).
- **B6**. Dos métodos de pago: PayPal Sandbox y contra-reembolso (3.5).
- **B7**. Correo de confirmación con código de seguimiento y datos de la reserva (3.5).
- **B8**. Tasa de combustible aplicada (50 €/día, excepto veleros) (3.5).
- **B9**. Estados de reserva y reglas de cancelación (3.6).
- **B10**. Seguimiento de reservas con código (3.7).
- **B11**. Gestión administrativa desde panel propio (3.8).

Se reporta el número de criterios B cumplidos sobre el total (11). Un fallo en Nivel B se registra como funcionalidad no implementada o implementada parcialmente; no impide evaluar el Nivel C.

### Nivel C — Empaquetado y despliegue

- **C1**. Existe un `Dockerfile` en el repositorio del producto.
- **C2**. El contenedor se construye sin errores siguiendo las instrucciones del README.
- **C3**. La aplicación arranca dentro del contenedor y es accesible en la URL documentada.
- **C4**. El README contiene instrucciones completas de construcción y arranque (incluyendo comandos concretos).

Un fallo en Nivel C se reporta explícitamente y se discute como hallazgo en el capítulo 9 de la memoria. Puede indicar una limitación del pipeline (o del modelo) para producir artefactos de despliegue, lo cual es un resultado interpretable en sí mismo.

### Nota sobre la evaluación

La UI debe estar íntegramente en español a lo largo de los niveles A, B y C. Si se detecta texto en otro idioma en elementos visibles de la interfaz (no en el código fuente), se reporta como incidencia pero no invalida el cumplimiento de los criterios funcionales.

---

## 7. Restricciones de proceso (para el pipeline IA)

- **El pipeline no puede ampliar el alcance definido en la sección 3 ni relajar las restricciones de la sección 4** para facilitar su propia ejecución. Cualquier desviación detectada en un gate humano debe resolverse mediante regeneración, no mediante modificación del brief.
- **El pipeline no tiene acceso a ninguna implementación, código, diseño o documentación del baseline humano**. Solo a este brief.
- Las decisiones de diseño técnico (estructura de apps Django, modelos de datos, rutas, plantillas) corresponden al agente Arquitecto y se derivan únicamente de este brief.
- El reparto de funcionalidades entre sprints lo decide el agente PM. El brief no fija ese reparto.

---

## 8. Notas de trazabilidad

Este brief se ha construido a partir de:

- Enunciado general del docente ("03 - Enunciado de la práctica.docx").
- Listado de funcionalidades del producto ("04 - Funcionalidad del producto.txt").
- Checklist de aceptación del docente (18+ ítems, fotografía en los materiales del proyecto).
- Actas de reunión con el patrocinador Jesús Torres (16 oct, 23 oct, 27 oct, 4 nov de 2024, Grupo G3.2).

Las funcionalidades propuestas en actas y **rechazadas** por el patrocinador (fianza del 20 %, no-devolución explícita como regla) no forman parte del alcance. Las funcionalidades implementadas por el baseline humano como mejoras no requeridas (múltiples imágenes por barco, despliegue en PaaS) tampoco forman parte del alcance obligatorio del pipeline IA.
