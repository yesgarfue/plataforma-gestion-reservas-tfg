---
run_id: run_2026-05-11_13-11
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-11T13:24:03+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-11_13-11`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Cubrir explícitamente el caso de 'velero' con un test unitario en el cálculo de la tasa de combustible antes de cerrar la historia HU-15, y añadir un comentario en el código que explique la excepción. |
| R-03 | SQLite tiene concurrencia limitada para múltiples reservas simultáneas, lo que puede causar bloqueos o pérdida de datos si varios clientes reservan al mismo tiempo. | media | alto | Implementar transacciones explícitas con nivel de aislamiento SERIALIZABLE en el modelo de reserva, ejecutar pruebas de carga con al menos 10 reservas concurrentes antes de cerrar el sprint 2, y documentar las limitaciones de SQLite en la guía de despliegue. |
| R-04 | El envío de correos de confirmación y recordatorio depende de un servidor SMTP configurado correctamente, que puede no estar disponible en el entorno de desarrollo o demo. | media | medio | Implementar un backend de correo en memoria (console backend) para desarrollo y pruebas, y crear un script de validación que verifique la configuración SMTP antes de cada despliegue en producción. |
| R-05 | Los datos seed (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, usuarios) deben cargarse de forma fiable en cada arranque del contenedor Docker, pero pueden fallar si las migraciones no se ejecutan correctamente. | media | medio | Crear un script de inicialización (entrypoint.sh) que ejecute manage.py migrate y manage.py loaddata en orden, con validación de errores, y añadir un test de integración que verifique que los datos seed están presentes tras el arranque. |
| R-06 | El proceso de reserva en tres pasos sin registro previo tiene múltiples casos borde (sesión expirada, datos incompletos, cambio de cesta durante el proceso) que pueden causar reservas inconsistentes. | alta | medio | Implementar un flujo de reserva con estado persistente en la sesión, crear tests de aceptación para cada caso borde (sesión expirada, volver atrás, cambiar cesta), y añadir validación de integridad antes de confirmar la reserva. |
| R-07 | Los filtros combinables del catálogo (puertos, fabricantes, precio, categoría, capacidad, rango de fechas) son más complejos de lo que aparentan y pueden generar queries SQL ineficientes o resultados incorrectos. | media | medio | Implementar los filtros de forma incremental en la historia HU-05, crear tests unitarios para cada combinación de filtros, y ejecutar EXPLAIN PLAN en las queries generadas para asegurar que usan índices correctamente. |
| R-08 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril de 2024), lo que puede causar vulnerabilidades de seguridad no parcheadas. | baja | alto | Ejecutar manage.py check --deploy antes de cada despliegue, aplicar todos los parches de seguridad disponibles para Django 3.2, y documentar un plan de migración a una versión más reciente de Django para después del lanzamiento inicial. |
| R-09 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, etc.) que pueden no estar disponibles o tener vulnerabilidades. | baja | medio | Especificar versiones exactas de las imágenes base en el Dockerfile (no usar 'latest'), ejecutar docker build en el pipeline de CI/CD antes de cada merge, y usar herramientas como Trivy para escanear vulnerabilidades en las imágenes. |
| R-10 | El reparto de funcionalidades entre tres sprints puede dejar dependencias cruzadas, por ejemplo el sprint 2 (pago) depende del modelo de reserva del sprint 1, lo que puede causar retrasos si el sprint 1 se retrasa. | media | medio | Implementar el modelo de reserva (HU-17) al inicio del sprint 1, crear un contrato de interfaz claro entre sprints, y ejecutar pruebas de integración entre sprints al final de cada uno para detectar incompatibilidades temprano. |
