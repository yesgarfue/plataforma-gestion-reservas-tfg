---
run_id: run_2026-05-14_19-50
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T20:09:30+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-14_19-50`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Cubrir explícitamente el caso de 'velero' con un test unitario en el cálculo de la tasa de combustible antes de cerrar la historia HU-10, y añadir un comentario en el código señalando la excepción. |
| R-03 | SQLite tiene concurrencia limitada para múltiples reservas simultáneas, lo que puede causar bloqueos o errores durante picos de uso o pruebas de carga. | media | alto | Implementar un test de concurrencia con al menos 10 reservas simultáneas en el Sprint 2 antes de cerrar HU-07. Si se detectan bloqueos, documentar la limitación y establecer un plan de migración a PostgreSQL para producción. |
| R-04 | El envío de correos de confirmación y recordatorio depende de un servidor SMTP configurado, que puede no estar disponible en el entorno de desarrollo o demo. | media | medio | Configurar un backend de correo en memoria (console backend) para desarrollo y pruebas, y crear un script de verificación que valide la configuración SMTP antes de cada despliegue en producción. |
| R-05 | El proceso de reserva en tres pasos sin registro previo tiene múltiples casos borde: cliente que inicia sesión a mitad del proceso, cesta que se modifica durante la reserva, datos heredados incompletos. | alta | medio | Crear un conjunto de test de integración en el Sprint 2 que cubra explícitamente: (1) login durante el proceso, (2) modificación de cesta antes de confirmar, (3) datos heredados parciales. Ejecutar estos tests antes de cerrar HU-07. |
| R-06 | Los filtros combinables del catálogo (puerto, fabricante, precio, categoría, capacidad, fechas) son complejos de implementar correctamente y pueden tener comportamientos inesperados con combinaciones específicas. | media | medio | Implementar tests parametrizados en el Sprint 1 que prueben al menos 15 combinaciones de filtros diferentes, incluyendo casos límite (rango de precio vacío, fechas invertidas, sin resultados). Documentar el comportamiento esperado en cada caso. |
| R-07 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024), lo que puede causar vulnerabilidades de seguridad no parcheadas o incompatibilidades con dependencias. | baja | alto | Ejecutar 'pip check' y 'safety check' antes de cada release para detectar vulnerabilidades conocidas. Documentar en el README que la aplicación requiere actualización a Django 4.2 LTS para producción. |
| R-08 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero pueden fallar si hay conflictos de claves primarias o cambios en el esquema. | media | medio | Crear un script de inicialización que primero ejecute 'python manage.py migrate' y luego 'python manage.py loaddata' con manejo de excepciones. Incluir en el Dockerfile un healthcheck que valide que los datos precargados existen. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, etc.) que pueden no estar disponibles o tener vulnerabilidades. | baja | medio | Especificar versiones exactas de imágenes base en el Dockerfile (p.ej. 'python:3.9.18-slim') en lugar de tags flotantes. Ejecutar 'docker scan' antes de cada release para detectar vulnerabilidades en capas. |
| R-10 | El reparto de funcionalidades entre tres sprints puede dejar dependencias cruzadas: el Sprint 2 (reserva y pago) depende del modelo de reserva del Sprint 1, y el Sprint 3 (cancelación y seguimiento) depende de ambos. | alta | medio | En el Sprint 1, implementar el modelo de Reserva completo con todos los campos (incluyendo código de seguimiento y estados) aunque no se use en la UI. Esto permite que el Sprint 2 comience sin bloqueos. Realizar una reunión de sincronización al cierre de cada sprint para validar que las dependencias están resueltas. |
