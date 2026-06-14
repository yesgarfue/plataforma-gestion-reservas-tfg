---
run_id: run_2026-05-13_06-57
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-13T07:09:29+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-13_06-57`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal en el Sprint 2, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Crear un test unitario explícito que valide el cálculo de tasa de combustible para barcos 'velero' (debe ser 0 €) y para otras categorías (debe ser 50 €/día) antes de cerrar HU-12 en el Sprint 2. |
| R-03 | SQLite tiene concurrencia limitada y puede generar bloqueos si múltiples clientes intentan reservar simultáneamente, especialmente durante demos o picos de uso. | media | alto | Implementar transacciones explícitas con SELECT FOR UPDATE en el modelo de Reserva para evitar condiciones de carrera, y ejecutar pruebas de carga con al menos 10 reservas concurrentes antes de cerrar el Sprint 2. |
| R-04 | El proceso de reserva en tres pasos sin registro previo tiene múltiples casos borde (sesión expirada, cambio de cesta durante el proceso, recuperación de cesta tras login) que pueden causar inconsistencias de datos. | alta | medio | Documentar explícitamente los tres casos borde en HU-04 y HU-10, crear tests de integración que cubran cada caso (sesión expirada, cambio de cesta, login durante reserva), y ejecutarlos antes de cerrar el Sprint 2. |
| R-05 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero las migraciones de Django pueden fallar si el esquema ya existe o si hay conflictos de dependencias. | media | medio | Crear un script de inicialización (manage.py seed) que primero ejecute migrate --noinput, luego cargue los datos seed de forma idempotente (verificar existencia antes de crear), y documentar el orden de ejecución en el Dockerfile antes de cerrar HU-24 en el Sprint 1. |
| R-06 | El envío de correos (confirmación de reserva, recordatorio, cancelación) depende de un servidor SMTP configurado que puede no estar disponible en desarrollo o en demos sin conexión a internet. | media | medio | Configurar Django para usar un backend de correo en memoria (console backend) en desarrollo y tests, y crear un fixture de correos capturados para validar que los correos se generan correctamente sin depender de SMTP real. |
| R-07 | Los filtros combinables (puertos, fabricantes, precio, categoría, capacidad, rango de fechas) son complejos de implementar correctamente, especialmente la lógica de disponibilidad por rango de fechas que requiere consultas a reservas existentes. | alta | medio | Implementar los filtros de forma incremental en HU-07: primero puertos y fabricante (desplegables simples), luego precio y categoría (filtros de rango), finalmente capacidad y rango de fechas (con subconsultas a reservas). Crear tests unitarios para cada combinación de filtros antes de cerrar el Sprint 1. |
| R-08 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024) y puede tener vulnerabilidades de seguridad no parcheadas o incompatibilidades con librerías modernas. | baja | alto | Ejecutar manage.py check --deploy antes de cada release, mantener un registro de dependencias pinned en requirements.txt, y revisar el changelog de Django 3.2 mensualmente para parches de seguridad críticos. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x) que pueden no estar disponibles o tener vulnerabilidades, y las dependencias de pip pueden fallar si los repositorios están caídos. | media | medio | Especificar versiones exactas de la imagen base (python:3.9-slim) en el Dockerfile, cachear las dependencias de pip en una capa intermedia, y crear un script de fallback que construya la imagen con un mirror local de pip si el repositorio oficial no está disponible. |
| R-10 | El reparto de funcionalidades entre tres sprints es ajustado y el Sprint 2 depende del modelo de Reserva y Cesta del Sprint 1, lo que puede causar retrasos en cascada si el Sprint 1 se atrasa. | media | alto | Definir explícitamente las interfaces de modelo (Barco, Reserva, Cesta) al final del Sprint 1 antes de que comience el Sprint 2, crear mocks de esas interfaces para que el Sprint 2 pueda desarrollar en paralelo, y ejecutar una integración de prueba entre sprints al final de la semana 1. |
