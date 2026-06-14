---
run_id: run_2026-05-12_16-48
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-12T17:01:38+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-12_16-48`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Cubrir explícitamente el caso de 'velero' con un test unitario en el cálculo de la tasa de combustible antes de cerrar la historia HU-12, y añadir un comentario en el código señalando la excepción. |
| R-03 | SQLite tiene concurrencia limitada para múltiples reservas simultáneas, lo que puede causar bloqueos o errores de transacción durante picos de uso. | media | alto | Implementar transacciones explícitas con isolation_level en Django para las operaciones críticas de reserva, y ejecutar pruebas de carga con al menos 10 reservas concurrentes antes de cerrar el sprint 2. |
| R-04 | El envío de correos de confirmación y recordatorio depende de un SMTP configurado en el entorno, que puede no estar disponible o mal configurado en desarrollo o demo. | alta | medio | Configurar un backend de correo en memoria (console backend) para desarrollo y testing, y documentar en el README la configuración de SMTP para producción. Implementar un log de correos no enviados para auditoría. |
| R-05 | Los filtros combinables (puertos, fabricantes, precio, categoría, capacidad, fechas) son más complejos de lo que aparentan, con múltiples casos borde en la combinación de criterios. | alta | medio | Crear un conjunto de tests de integración en la historia HU-06 que cubra al menos 15 combinaciones de filtros diferentes, incluyendo casos límite como rango de precios vacío, fechas inválidas y ausencia de resultados. |
| R-06 | El proceso de reserva en tres pasos sin registro previo tiene casos borde complejos, como la reconstrucción de cesta al iniciar sesión durante el proceso o la validación de datos incompletos. | media | medio | Documentar explícitamente el flujo de sesión durante la reserva en la historia HU-02 y HU-09, crear tests de integración que cubran el inicio de sesión a mitad del proceso, y validar que la cesta se reconstruye correctamente. |
| R-07 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero pueden fallar si hay conflictos de claves primarias o cambios en el esquema. | media | medio | Crear un script de carga de datos que primero ejecute 'python manage.py flush --no-input' para limpiar la base de datos, luego cargue los datos seed, y verificar que el contenedor Docker ejecuta este script automáticamente en el entrypoint. |
| R-08 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024), lo que puede causar vulnerabilidades de seguridad no parcheadas. | baja | alto | Documentar en el README que Django 3.2 es una versión heredada y que se recomienda actualizar a una versión LTS más reciente en producción. Ejecutar 'python manage.py check --deploy' antes de cada release para identificar problemas de seguridad. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas que pueden no estar disponibles o cambiar de forma incompatible. | baja | medio | Especificar versiones exactas de las imágenes base en el Dockerfile (p.ej. 'python:3.9-slim' en lugar de 'python:latest'), y documentar las versiones probadas en el README. |
| R-10 | Tres sprints son ajustados para el alcance comprometido, y el reparto entre sprints puede dejar dependencias cruzadas que bloqueen el desarrollo (p.ej. el sprint 2 necesita el modelo de reserva del sprint 1). | media | alto | Ejecutar una reunión de planificación de dependencias al inicio del sprint 1 para identificar y documentar todas las dependencias entre historias. Priorizar las historias de modelo de datos (HU-13) en el sprint 1 aunque no sean visibles al usuario, para desbloquear el sprint 2. |
