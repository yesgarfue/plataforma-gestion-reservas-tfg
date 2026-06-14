---
gate: 3
fase: 03_arquitectura
decision: aceptado
timestamp_revision_inicio: 2026-05-17T19:27:40+02:00
timestamp_revision_fin: 2026-05-17T19:43:40+02:00
---

## Observaciones

Artefacto revisado: `diseno_tecnico.json` / `diseno_tecnico.md`.

La regeneracion corrige el problema bloqueante detectado en la primera version del diseño tecnico. El panel administrativo propio queda ahora expuesto bajo `/admin-panel/` y sus subrutas, evitando ocupar `/admin/` como panel custom. Esto es coherente con el contrato ejecutable congelado, que exige `/admin-panel/` para el panel propio y reserva `/admin/` para el admin Django.

El diseño mantiene las rutas canonicas principales exigidas para validacion: `/`, `/barcos/`, `/cesta/`, `/accounts/registro/`, `/accounts/login/`, `/reserva/paso1/`, `/reserva/paso2/`, `/reserva/paso3/`, `/seguimiento/` y `/admin-panel/`.

PayPal queda definido como flujo Sandbox simulado y reproducible, sin dependencia obligatoria de API externa, lo cual es adecuado para el entorno de validacion del pipeline.

La arquitectura define apps razonables para autenticacion, catalogo, cesta, reservas, panel administrativo y core. Tambien contempla `core/management/commands/seed_data.py`, por lo que en desarrollo debera asegurarse que `core` este incluido en `INSTALLED_APPS`.

Observaciones no bloqueantes:

- La regeneracion modifica el modelo de datos: desaparece `ItemCarrito` como modelo persistente y se introduce `LineaReserva` asociada a `Reserva`. Esto es aceptable si la cesta se gestiona mediante sesion y `cart/services.py`, pero debe vigilarse que la cesta funcione correctamente entre seleccion, login durante reserva y confirmacion.
- El modelo `Reserva` ya no enlaza directamente con `Barco`; la relacion se desplaza a `LineaReserva`. Esta decision es coherente para guardar lineas de reserva, cantidades, precio unitario y tasa historica, pero aumenta ligeramente la complejidad del desarrollo.
- Los estados `EN_USO` y `DEVUELTO` siguen ampliando el ciclo minimo requerido por el brief. No bloquea, pero debe evitarse que complique el flujo basico de pago, cancelacion y seguimiento.
- La ruta `/admin/` no aparece listada explicitamente en el diseño regenerado. Debe conservarse mediante el admin Django estandar en `core/urls.py` o configuracion equivalente.

Decision: aceptado con observaciones porque la arquitectura ya respeta las rutas canonicas principales, corrige el conflicto del panel administrativo y ofrece una base tecnica suficiente para iniciar scaffold y desarrollo.


## Acción

Ninguna.