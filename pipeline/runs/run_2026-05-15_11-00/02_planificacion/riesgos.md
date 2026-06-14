---
run_id: run_2026-05-15_11-00
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-15T11:04:48+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-15_11-00`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Cubrir explícitamente el caso de 'velero' con un test unitario en el cálculo de la tasa de combustible antes de cerrar la historia HU-12, y añadir un comentario en el código señalando la excepción. |
| R-03 | SQLite tiene concurrencia limitada para múltiples reservas simultáneas, lo que puede causar bloqueos o pérdida de datos si varios clientes reservan al mismo tiempo. | media | alto | Implementar transacciones explícitas con nivel de aislamiento SERIALIZABLE en el modelo de reserva, y ejecutar pruebas de carga con al menos 10 reservas concurrentes antes de cerrar el Sprint 2. |
| R-04 | El proceso de reserva en tres pasos sin registro previo tiene múltiples casos borde: cliente que inicia sesión a mitad del proceso, cesta que se pierde, datos heredados inconsistentes. | alta | medio | Crear un documento de casos borde para HU-09 y HU-22 antes de comenzar el desarrollo, y ejecutar pruebas manuales de flujos cruzados (login durante reserva, cambio de datos, cancelación) antes de cerrar el Sprint 2. |
| R-05 | Los filtros combinables de catálogo (puerto, fabricante, precio, categoría, capacidad, fechas) son más complejos de lo que aparentan, con riesgo de queries ineficientes o resultados incorrectos. | media | medio | Implementar los filtros con índices de base de datos en los campos filtrados, y crear tests de integración que validen cada combinación de filtros (al menos 5 combinaciones) antes de cerrar HU-06 en el Sprint 1. |
| R-06 | El envío de correos (confirmación de reserva, recordatorio de pago, cancelación) depende de un SMTP configurado correctamente, que puede no estar disponible en desarrollo o en producción. | media | medio | Configurar un backend de correo en memoria (console backend) para desarrollo y testing, y crear un script de validación que verifique la configuración SMTP antes de cada arranque de la aplicación. |
| R-07 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024), lo que puede causar vulnerabilidades de seguridad no parcheadas. | baja | alto | Ejecutar 'pip check' y 'safety check' en cada commit para detectar dependencias vulnerables, y documentar en el README que la aplicación requiere actualizaciones de seguridad periódicas. |
| R-08 | Los datos seed (mínimo 5 barcos, 2 puertos, 2 fabricantes, 2 categorías incluyendo velero, 1 admin, 1 cliente) deben cargarse de forma fiable en cada arranque del contenedor Docker. | media | medio | Crear un script de inicialización (manage.py seed) que sea idempotente y se ejecute automáticamente en el entrypoint del Dockerfile, con validación de que los datos existen antes de crear duplicados. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, etc.) que pueden no estar disponibles o tener vulnerabilidades. | baja | medio | Especificar versiones exactas de imágenes base en el Dockerfile (no 'latest'), y ejecutar 'docker build' con '--pull' en cada construcción para obtener las últimas actualizaciones de seguridad. |
| R-10 | Tres sprints son ajustados para el alcance comprometido (23 historias), con riesgo de que dependencias cruzadas entre sprints (p.ej. Sprint 2 necesita modelo de reserva de Sprint 1) causen retrasos. | alta | medio | Realizar una reunión de planificación de dependencias antes de comenzar el Sprint 1, identificar explícitamente qué historias del Sprint 1 son bloqueantes para el Sprint 2, y ejecutar daily standups enfocados en dependencias. |
