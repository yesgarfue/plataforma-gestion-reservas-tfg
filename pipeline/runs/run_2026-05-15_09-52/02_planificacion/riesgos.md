---
run_id: run_2026-05-15_09-52
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-15T09:58:14+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-15_09-52`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total de la reserva. | alta | medio | Cubrir explícitamente el caso de 'velero' con un test unitario en el cálculo de la tasa de combustible antes de cerrar la historia HU-11, y añadir un comentario en el código señalando la excepción. |
| R-03 | SQLite tiene concurrencia limitada y puede generar bloqueos si múltiples clientes intentan reservar simultáneamente, causando errores de transacción. | media | alto | Implementar reintentos automáticos con backoff exponencial en las operaciones de reserva, y documentar en el README que SQLite es adecuado solo para desarrollo y pruebas, no para producción con alto volumen. |
| R-04 | El envío de correos de confirmación y recordatorio depende de un servidor SMTP configurado, que puede no estar disponible en el entorno de desarrollo o demo. | alta | medio | Configurar un backend de correo en memoria (console backend) por defecto en desarrollo, y crear un fixture de prueba que simule el envío sin depender de SMTP externo. Documentar la configuración de SMTP en el README. |
| R-05 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero si el script de carga falla silenciosamente, la aplicación arrancará sin datos de ejemplo. | media | medio | Crear un comando Django personalizado (manage.py load_seed_data) que verifique la existencia de datos y lance una excepción si la carga falla. Ejecutar este comando en el entrypoint del Dockerfile y bloquear el arranque si falla. |
| R-06 | El proceso de reserva en tres pasos sin registro previo tiene múltiples casos borde: cliente que inicia sesión a mitad del proceso, cesta que se vacía al cambiar de rol, datos heredados incompletos. | alta | medio | Crear un conjunto exhaustivo de tests de integración que cubra los flujos: reserva sin sesión, login durante reserva, cambio de rol, recuperación de cesta. Ejecutar estos tests en cada commit del sprint 2. |
| R-07 | Los filtros combinables (puerto, fabricante, precio, categoría, capacidad, fechas) son complejos de implementar correctamente y pueden generar queries SQL ineficientes o resultados incorrectos. | media | medio | Implementar los filtros de forma incremental en la historia HU-04, comenzando con filtros simples (puerto, fabricante) y añadiendo complejidad (rango de fechas, disponibilidad). Incluir tests de filtrado para cada combinación crítica. |
| R-08 | Django 3.2 es una versión antigua con soporte limitado y puede tener vulnerabilidades de seguridad no parcheadas o incompatibilidades con dependencias modernas. | baja | alto | Documentar explícitamente en el README que Django 3.2 es una versión heredada y que la aplicación es solo para propósitos educativos. Ejecutar un análisis de dependencias con 'pip-audit' antes de cada release y documentar cualquier vulnerabilidad conocida. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, etc.) que pueden no estar disponibles o cambiar de forma incompatible. | baja | medio | Fijar versiones específicas de imágenes base en el Dockerfile (p.ej. python:3.9-slim-bullseye) en lugar de usar tags flotantes. Documentar las versiones esperadas en el README. |
| R-10 | El reparto de funcionalidades entre sprints puede dejar dependencias cruzadas: el sprint 2 (reserva y pago) depende del modelo de barco y cesta del sprint 1, y el sprint 3 (cancelación y seguimiento) depende del modelo de reserva del sprint 2. | alta | medio | Asegurar que al cierre del sprint 1 el modelo de barco, cesta y autenticación están completamente funcionales y testeados. Realizar una revisión de dependencias entre sprints al inicio del proyecto y ajustar el plan si es necesario. |
