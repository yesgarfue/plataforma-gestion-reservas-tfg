---
run_id: run_2026-05-11_13-31
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-11T14:23:01+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-11_13-31`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | El servidor SMTP para envío de correos de confirmación puede no estar configurado o disponible en el entorno de desarrollo o producción, impidiendo que los clientes reciban el código de seguimiento. | media | alto | Configurar un servicio SMTP de prueba (p.ej. MailHog o SendGrid sandbox) en el Dockerfile y documentar en el README los pasos para configurar SMTP en producción. Implementar logs de correos fallidos para detectar problemas rápidamente. |
| R-03 | SQLite tiene limitaciones de concurrencia que pueden causar bloqueos o pérdida de datos si múltiples clientes intentan reservar el mismo barco simultáneamente. | alta | alto | Implementar transacciones explícitas con nivel de aislamiento SERIALIZABLE en el modelo de reserva. Añadir tests de carga con al menos 10 reservas simultáneas del mismo barco antes de cerrar el sprint 2. Documentar en el README que SQLite es solo para desarrollo y que se debe migrar a PostgreSQL para producción. |
| R-04 | El proceso de reserva en tres pasos sin registro previo tiene casos borde complejos: recuperación de cesta al iniciar sesión durante la reserva, conflictos entre cesta anterior y actual, y validación de datos de contacto incompletos. | alta | medio | Crear un documento de casos de prueba exhaustivos para el flujo de reserva sin registro (incluyendo sesión iniciada a mitad del proceso, datos inválidos, cambios de cantidad). Ejecutar pruebas manuales de estos casos antes de cerrar el sprint 2. Implementar validación de datos de contacto con mensajes de error específicos. |
| R-05 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024), lo que puede causar vulnerabilidades de seguridad no parcheadas y incompatibilidades con librerías modernas. | media | medio | Ejecutar 'pip check' y 'safety check' antes de cada commit para detectar dependencias vulnerables. Documentar en el README que la aplicación está construida con Django 3.2 y que se recomienda migrar a una versión LTS más reciente (Django 4.2 o superior) antes de desplegar a producción. |
| R-06 | Los datos seed (barcos, categorías) deben cargarse de forma fiable en cada arranque del contenedor Docker, pero si el script de carga falla silenciosamente, la aplicación arrancará sin datos y parecerá funcional pero vacía. | media | medio | Crear un script manage.py seed que verifique la existencia de datos y los cargue si no existen. Añadir un health check en el Dockerfile que valide que existen al menos 5 barcos en la base de datos. Documentar en el README cómo cargar datos manualmente si es necesario. |
| R-07 | El filtrado combinable de barcos por puerto, fabricante, precio, categoría, capacidad y fechas es más complejo de lo que aparenta, con riesgo de queries ineficientes o resultados incorrectos cuando se combinan múltiples filtros. | media | medio | Implementar tests unitarios para cada combinación de filtros (al menos 8 combinaciones) antes de cerrar el sprint 1. Usar Django ORM con select_related y prefetch_related para optimizar queries. Medir tiempo de respuesta con 1000+ barcos en la base de datos. |
| R-08 | El reparto de funcionalidades entre sprints crea dependencias cruzadas: el sprint 2 (pago) depende del modelo de reserva del sprint 1, y el sprint 3 (cancelación) depende de ambos. | alta | medio | Definir el modelo de Reserva con todos sus campos (incluyendo estado, código de seguimiento, fechas) en el sprint 1, aunque no se use completamente hasta el sprint 2. Realizar integración continua entre sprints: al final del sprint 1, verificar que el sprint 2 puede construir sobre el código entregado sin cambios de modelo. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, etc.) que pueden no estar disponibles o tener vulnerabilidades de seguridad. | baja | medio | Especificar versiones exactas de imágenes base en el Dockerfile (p.ej. python:3.9-slim-bullseye en lugar de python:3.9). Ejecutar 'docker scan' antes de cada release para detectar vulnerabilidades. Documentar en el README cómo construir la imagen con un registro privado si es necesario. |
| R-10 | El código de seguimiento debe ser único y no predecible, pero si se genera de forma insegura (p.ej. secuencial o con baja entropía), un cliente podría adivinar códigos de otros clientes. | baja | alto | Generar códigos de seguimiento usando uuid.uuid4() o secrets.token_urlsafe(16). Añadir un test unitario que verifique que 1000 códigos generados son todos únicos. Documentar en el código que los códigos deben ser criptográficamente seguros. |
