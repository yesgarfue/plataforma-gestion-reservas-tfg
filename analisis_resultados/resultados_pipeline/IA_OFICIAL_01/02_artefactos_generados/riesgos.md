---
run_id: run_2026-05-18_15-09
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-18T15:29:57+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-18_15-09`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | [Proyecto] PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. Verificar en el check mínimo del Sprint 2 que contra-reembolso es seleccionable y funciona sin PayPal. |
| R-02 | [Sprint 2] La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Cubrir explícitamente el caso de 'velero' con un test unitario en el cálculo de la tasa de combustible antes de cerrar HU-11. El test debe validar que veleros aplican 0 € y otros barcos aplican 50 €/día. Bloquear merge de HU-11 si el test no pasa. |
| R-03 | [Sprint 1] Los filtros combinables (puerto, fabricante, precio, categoría, capacidad, fechas) son más complejos de lo que aparentan y pueden tener casos borde en la combinación de criterios. | alta | medio | Implementar tests de integración para HU-05 que cubran al menos 5 combinaciones de filtros (p.ej. puerto + precio, fabricante + capacidad + fechas). Ejecutar manage.py test antes de cerrar Sprint 1 y bloquear merge si alguna combinación falla. |
| R-04 | [Sprint 2] El proceso de reserva en 3 pasos sin registro previo tiene casos borde: cliente inicia sesión durante el proceso, cesta debe recuperarse, datos deben heredarse correctamente. | media | alto | Crear un test de flujo end-to-end en HU-08 que simule: (1) cliente anónimo añade barco a cesta, (2) inicia sesión en mitad del proceso, (3) vuelve de login y cesta persiste, (4) datos del cliente se heredan. Ejecutar antes de cerrar Sprint 2. |
| R-05 | [Proyecto] SQLite tiene concurrencia limitada para reservas simultáneas, lo que puede causar bloqueos si múltiples clientes reservan al mismo tiempo. | media | medio | Documentar en el README que SQLite es adecuado para desarrollo y pruebas, pero no para producción con alto volumen. Implementar transacciones explícitas en el modelo de Reserva usando transaction.atomic() para minimizar bloqueos. Ejecutar manage.py check antes de cada commit. |
| R-06 | [Proyecto] El envío de correos (confirmación de reserva, recordatorio de pago) depende de un SMTP configurado correctamente en el entorno, que puede no estar disponible durante desarrollo. | alta | medio | Configurar Django para usar console backend en desarrollo (EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend') para que los correos se impriman en consola sin SMTP real. En producción, usar un SMTP válido. Verificar en checks mínimos de Sprint 2 y Sprint 3 que los correos se generan correctamente. |
| R-07 | [Proyecto] Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero si el script de seed falla, la aplicación arranca sin datos de prueba. | media | bajo | Crear un comando manage.py seed_data que sea idempotente (no falla si los datos ya existen). Ejecutarlo en el Dockerfile con RUN python manage.py seed_data después de migrate. Verificar en el check mínimo de Sprint 1 que manage.py seed_data se ejecuta sin errores y carga al menos 5 barcos. |
| R-08 | [Proyecto] Django 3.2 es una versión antigua con soporte limitado (LTS hasta abril 2024), lo que puede causar vulnerabilidades de seguridad no parcheadas. | baja | alto | Documentar en el README que Django 3.2 es la versión especificada por el proyecto y que en producción debe evaluarse una migración a una versión LTS más reciente. Ejecutar manage.py check --deploy antes de cada release para detectar problemas de seguridad conocidos. |
| R-09 | [Sprint 3] El sistema de correos automáticos de recordatorio (HU-14) depende de una tarea programada (celery beat o similar) que puede no ejecutarse si no está configurada correctamente. | media | medio | Implementar el recordatorio como un comando manage.py que se ejecuta vía cron o celery beat. Documentar en el README cómo configurar la tarea. Crear un test que simule la ejecución del comando y verifique que se envía un correo cuando falta 1 día para el inicio de la reserva. |
| R-10 | [Sprint 3] La restricción de eliminación de clientes con reservas pendientes (HU-18) puede no validarse correctamente, permitiendo eliminar clientes con datos de auditoría importantes. | media | medio | Implementar una validación explícita en el modelo Cliente que lance una excepción si se intenta eliminar un cliente con reservas en estado PENDIENTE DE PAGO. Crear un test unitario que verifique que la eliminación falla cuando hay reservas pendientes. Bloquear merge de HU-18 si el test no pasa. |
