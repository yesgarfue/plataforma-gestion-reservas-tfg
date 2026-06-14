---
run_id: run_2026-05-14_16-05
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T16:10:05+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-14_16-05`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Cubrir explícitamente el caso de 'velero' con un test unitario en el cálculo de la tasa de combustible antes de cerrar la historia HU-12, y añadir un comentario en el código señalando la excepción. |
| R-03 | SQLite tiene concurrencia limitada para múltiples reservas simultáneas, lo que puede causar bloqueos o pérdida de datos si varios clientes completan reservas al mismo tiempo. | media | alto | Implementar transacciones explícitas con nivel de aislamiento SERIALIZABLE en el modelo de Reserva, y ejecutar pruebas de carga con al menos 10 reservas concurrentes antes de cerrar el Sprint 2. |
| R-04 | El envío de correos de confirmación y recordatorio depende de un servidor SMTP configurado, que puede no estar disponible en el entorno de desarrollo o demo. | media | medio | Configurar un backend de correo en memoria (console backend) para desarrollo y pruebas, y documentar en el README los pasos para configurar un SMTP real en producción. Verificar que los correos se generan correctamente aunque no se envíen. |
| R-05 | Los filtros combinables de puertos, fabricantes, precio, categoría, capacidad y rango de fechas son más complejos de lo que aparentan, con múltiples casos borde en las consultas a la base de datos. | alta | medio | Crear un conjunto exhaustivo de tests de integración para HU-04 cubriendo al menos 15 combinaciones de filtros (incluyendo filtros vacíos, rangos de precio inválidos, fechas sin disponibilidad), y ejecutarlos antes de cerrar el Sprint 1. |
| R-06 | El proceso de reserva en tres pasos sin registro previo tiene casos borde complejos: cliente inicia sesión a mitad del proceso, cesta se pierde, datos heredados no se sincronizan correctamente. | media | alto | Documentar explícitamente el flujo de sesión durante la reserva en un diagrama de estados, implementar tests de aceptación para los tres escenarios críticos (sin sesión, login a mitad, sesión preexistente) antes de cerrar HU-13, y usar sesiones de Django con almacenamiento en base de datos. |
| R-07 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024), lo que puede dificultar la resolución de vulnerabilidades de seguridad o bugs críticos. | baja | medio | Documentar en el README que Django 3.2 es la versión especificada por requisito, ejecutar manage.py check antes de cada commit y bloquear merge si hay advertencias de seguridad, y mantener un registro de parches de seguridad aplicados. |
| R-08 | Los datos seed (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, usuarios de prueba) deben cargarse de forma fiable en cada arranque del contenedor Docker, pero pueden no persistir o corromperse. | media | medio | Crear un script de inicialización (manage.py seed) que sea idempotente y se ejecute automáticamente en el entrypoint del Dockerfile. Verificar que los datos seed se cargan correctamente en tres arranques consecutivos del contenedor. |
| R-09 | El reparto de funcionalidades entre tres sprints puede dejar dependencias cruzadas: el Sprint 2 (pago) depende del modelo de Reserva del Sprint 1, y el Sprint 3 (admin) depende de ambos. | alta | medio | Ejecutar una revisión de dependencias entre sprints al cierre del Sprint 1, asegurando que el modelo de Reserva está completamente estable. Implementar un contrato de API clara entre sprints y ejecutar tests de integración entre Sprint 1 y Sprint 2 antes de cerrar Sprint 2. |
| R-10 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, postgres si se usa) que pueden no estar disponibles o tener vulnerabilidades de seguridad. | baja | medio | Especificar versiones exactas de imágenes base en el Dockerfile (p.ej. python:3.9.18-slim), ejecutar docker build en un entorno aislado antes de cada release, y documentar en el README cómo construir el contenedor sin acceso a internet usando un registro local. |
