---
run_id: run_2026-05-13_15-33
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-13T15:47:23+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-13_15-33`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago en línea. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Crear un test unitario explícito que valide que la tasa de combustible es 0 € para barcos de categoría 'velero' y 50 € para el resto, ejecutándolo antes de cerrar la historia HU-13. |
| R-03 | SQLite tiene concurrencia limitada y puede generar bloqueos si múltiples clientes intentan reservar simultáneamente, especialmente durante demostraciones o picos de uso. | media | alto | Implementar un mecanismo de transacciones explícitas con aislamiento SERIALIZABLE en el modelo de Reserva; documentar en el README que SQLite es adecuado solo para desarrollo y pruebas, no para producción con alto volumen. |
| R-04 | El envío de correos (confirmación, recordatorio de pago) depende de un servidor SMTP configurado que puede no estar disponible en el entorno de desarrollo o demo. | alta | medio | Implementar un backend de correo en memoria (console backend) por defecto en desarrollo; crear un fixture de prueba que valide que los correos se generan correctamente sin requerir SMTP real; documentar la configuración de SMTP en el README. |
| R-05 | Los filtros combinables (puertos, fabricantes, precio, categoría, capacidad, fechas) son más complejos de lo que aparentan, con múltiples casos borde en la combinación de filtros y en la lógica de disponibilidad por fechas. | alta | medio | Crear un conjunto exhaustivo de tests de integración para HU-06 que cubra al menos 10 combinaciones de filtros diferentes, incluyendo casos borde como rango de precios vacío, fechas sin disponibilidad y filtros sin resultados. |
| R-06 | El proceso de reserva en tres pasos sin registro previo tiene múltiples casos borde: cliente que inicia sesión a mitad del flujo, validación de datos incompletos, manejo de sesiones expiradas durante el proceso. | media | medio | Documentar explícitamente los tres pasos en HU-10 con diagramas de flujo; crear tests de integración que simulen iniciar sesión en el paso 2, abandonar y reanudar, y expiración de sesión. |
| R-07 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024) y puede tener vulnerabilidades de seguridad no parcheadas. | baja | alto | Documentar en el README que Django 3.2 es la versión especificada por requisito y que la aplicación es solo para demostración; ejecutar manage.py check --deploy antes de cada release y revisar el changelog de seguridad de Django 3.2 mensualmente. |
| R-08 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero pueden fallar si hay conflictos de claves primarias o cambios en el esquema. | media | medio | Crear un script de inicialización que ejecute flush antes de cargar los datos seed; incluir en el Dockerfile un healthcheck que valide que los datos seed están presentes (p.ej. verificar que existen al menos 5 barcos). |
| R-09 | Tres sprints son ajustados para el alcance comprometido; el sprint 2 depende del modelo de Reserva del sprint 1, y el sprint 3 depende de la lógica de estados del sprint 2, creando dependencias cruzadas que pueden bloquear el desarrollo. | media | alto | Definir el modelo de Reserva completo (con campos para estado, código de seguimiento, fechas, cliente, barco) en la primera semana del sprint 1; crear un stub funcional del flujo de pago en sprint 1 para que sprint 2 pueda comenzar en paralelo. |
| R-10 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, etc.) que pueden no estar disponibles o tener vulnerabilidades. | baja | medio | Especificar versiones exactas de imágenes base en el Dockerfile (p.ej. python:3.9.18-slim); ejecutar docker build con --pull para obtener la última versión de la imagen base; incluir un script de verificación de vulnerabilidades con trivy en el CI/CD. |
