---
run_id: run_2026-05-14_02-35
fase: 02_planificacion
agente: PM
modelo: anthropic/claude-haiku-4-5
timestamp: 2026-05-14T02:43:53+02:00
hash_brief: e62bcd5b2a4f56841065a31fe202de9d8628e317db0846675e689257a2eeb394
regeneraciones_previas: 0
---

# 02 — Registro de riesgos

**ID de ejecución**: `run_2026-05-14_02-35`

Total de riesgos: **10**

| ID | Descripción | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R-01 | PayPal Sandbox puede no estar disponible durante una demo o durante el desarrollo, bloqueando la prueba del flujo de pago integrado. | media | alto | Implementar y dejar completamente funcional el flujo de contra-reembolso antes de abordar la integración con PayPal, para que la aplicación sea demoable aunque la pasarela falle. |
| R-02 | La tasa de combustible tiene una excepción para barcos de categoría 'velero' (0 € en lugar de 50 €/día) que es fácil de olvidar al implementar el cálculo del importe total. | alta | medio | Crear un test unitario explícito que valide el cálculo de tarifa para barcos de categoría velero antes de cerrar la historia HU-11, y añadir un comentario en el código señalando la excepción. |
| R-03 | SQLite tiene concurrencia limitada y puede generar bloqueos si múltiples clientes intentan reservar simultáneamente, especialmente durante demostraciones o picos de uso. | media | alto | Implementar un mecanismo de transacciones explícitas con aislamiento SERIALIZABLE en el modelo de Reserva, y ejecutar pruebas de carga con al menos 10 reservas simultáneas antes de cerrar el Sprint 2. |
| R-04 | El envío de correos electrónicos (confirmación de reserva, recordatorios, notificaciones) depende de un servidor SMTP configurado que puede no estar disponible en el entorno de desarrollo o demo. | alta | medio | Configurar un backend de correo en memoria (console backend) para desarrollo y pruebas, y documentar en el README la configuración de SMTP para producción. Implementar un log de correos fallidos para auditoría. |
| R-05 | Los filtros combinables de puertos, fabricantes, precio, categoría, capacidad y rango de fechas son más complejos de lo que aparentan, con múltiples casos borde en la lógica de disponibilidad. | alta | medio | Crear un conjunto de tests de integración que cubra al menos 15 combinaciones de filtros diferentes, incluyendo casos borde como rango de fechas vacío, precio mínimo igual a máximo, y capacidad sin barcos disponibles. |
| R-06 | El proceso de reserva en tres pasos sin registro previo tiene casos borde complejos: cliente inicia sesión durante el proceso, recupera cesta, pero los datos de pago pueden no sincronizarse correctamente. | media | alto | Implementar un flujo de sesión con tokens CSRF persistentes en la cesta y ejecutar pruebas de usuario que simulen login durante el proceso de reserva antes de cerrar el Sprint 2. |
| R-07 | Django 3.2 es una versión antigua con soporte limitado (fin de soporte en abril 2024) y puede tener vulnerabilidades de seguridad no parcheadas. | baja | alto | Ejecutar manage.py check antes de cada commit y bloquear merge si hay advertencias de seguridad. Documentar en el README que la aplicación requiere actualizaciones de seguridad periódicas y que Django 3.2 debe ser reemplazado por una versión LTS más reciente en producción. |
| R-08 | Los datos seed deben cargarse de forma fiable en cada arranque del contenedor Docker, pero un fallo en la carga puede dejar la base de datos en estado inconsistente. | media | medio | Crear un script de inicialización que valide la integridad de los datos seed (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, usuarios de prueba) y lance una excepción si alguno falta. Ejecutar este script en el entrypoint del Dockerfile. |
| R-09 | Tres sprints son ajustados para el alcance comprometido, y el reparto entre sprints puede dejar dependencias cruzadas: el Sprint 2 (pago) depende del modelo de Reserva del Sprint 1, y el Sprint 3 (administración) depende de ambos. | alta | medio | Completar el modelo de Reserva con todos sus estados (PENDIENTE DE PAGO, PAGADO, EN USO, DEVUELTO) y transiciones válidas en el Sprint 1, antes de iniciar el Sprint 2. Realizar una revisión de arquitectura al cierre del Sprint 1 para validar que no hay bloqueos. |
| R-10 | La construcción del contenedor Docker depende de imágenes base externas (python:3.x, postgres o similar) que pueden no estar disponibles o tener vulnerabilidades. | media | medio | Especificar versiones exactas de imágenes base en el Dockerfile (p.ej. python:3.9-slim-bullseye) y ejecutar docker build con --pull para obtener la última versión segura. Documentar en el README las versiones mínimas requeridas. |
