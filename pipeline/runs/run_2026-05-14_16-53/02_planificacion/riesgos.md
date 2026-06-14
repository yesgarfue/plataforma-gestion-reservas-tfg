---
run_id: run_2026-05-14_16-53
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T17:07:30+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-14_16-53`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Cubrir explícitamente el caso de 'velero' con un test unitario en el cálculo de la tasa de combustible antes de cerrar la historia HU-10, y añadir un comentario en el código señalando la excepción. |
| R-03 | SQLite tiene concurrencia limitada para múltiples reservas simultáneas, lo que puede causar bloqueos o pérdida de datos si varios clientes reservan al mismo tiempo. | media | alto | Implementar transacciones explícitas con nivel de aislamiento SERIALIZABLE en el modelo de reserva, y ejecutar pruebas de carga con al menos 10 reservas concurrentes antes de cerrar el sprint 2. |
| R-04 | El proceso de reserva en 3 pasos sin registro previo tiene múltiples casos borde: cliente que inicia sesión a mitad del proceso, cesta que se vacía al cambiar de rol, datos heredados incompletos. | alta | medio | Crear un conjunto de test de integración que cubra explícitamente: (1) login durante reserva con cesta persistente, (2) vaciado de cesta al entrar en modo admin, (3) herencia de datos de sesión. Ejecutar estos tests antes de cerrar HU-20. |
| R-05 | Los filtros combinables del catálogo (puerto, fabricante, precio, categoría, capacidad, fechas) son complejos de implementar correctamente; las combinaciones pueden generar queries ineficientes o resultados incorrectos. | media | medio | Implementar los filtros de forma incremental en HU-04 con tests unitarios para cada combinación de filtros (al menos 8 combinaciones). Usar Django ORM con select_related y prefetch_related para optimizar queries, y medir tiempo de respuesta con datos seed. |
| R-06 | El envío de correos (confirmación de reserva, recordatorio, cancelación) depende de un SMTP configurado correctamente en el entorno, que puede no estar disponible o mal configurado. | media | medio | Implementar un backend de correo en memoria (console backend) para desarrollo y testing. En producción, usar variables de entorno para SMTP. Crear un test que verifique que cada correo se envía correctamente sin fallar la transacción de reserva. |
| R-07 | Django 3.2 es una versión antigua con soporte limitado (LTS hasta abril 2024), lo que puede causar vulnerabilidades de seguridad no parcheadas o incompatibilidades con dependencias nuevas. | baja | alto | Ejecutar 'pip check' y 'safety check' en cada build de Docker para detectar vulnerabilidades conocidas. Documentar en README que Django 3.2 es versión legacy y que se recomienda actualizar a Django 4.2+ para producción. |
| R-08 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker; si el script de carga falla, la aplicación arranca sin datos de prueba. | media | medio | Crear un script de carga de datos (manage.py loaddata o fixture JSON) que sea idempotente. Ejecutar el script en el Dockerfile con RUN manage.py loaddata seed_data, y añadir un health check que verifique que existen al menos 5 barcos antes de considerar el contenedor listo. |
| R-09 | El reparto de funcionalidades entre sprints deja dependencias cruzadas: el sprint 2 (reserva y pago) depende del modelo de barco y cesta del sprint 1, y el sprint 3 (cancelación y seguimiento) depende del modelo de reserva del sprint 2. | alta | medio | Asegurar que al cierre del sprint 1, el modelo de barco, cesta y autenticación están completamente funcionales con tests de integración. Bloquear el inicio del sprint 2 hasta que todos los tests del sprint 1 pasen. Usar integración continua (CI) para detectar regresiones. |
| R-10 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, postgres si se usa) que pueden no estar disponibles o tener vulnerabilidades. | baja | medio | Especificar versiones exactas de imágenes base en el Dockerfile (p.ej. python:3.9-slim-bullseye). Ejecutar 'docker scan' en el build para detectar vulnerabilidades. Documentar en README cómo construir offline si es necesario. |
