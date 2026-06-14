# Hundidos - Alquiler de Barcos

Aplicación web monolítica de alquiler de barcos construida con Django 3.2, SQLite y PayPal Sandbox.

## Instalación

### Requisitos previos
- Python 3.9+
- pip
- virtualenv (opcional pero recomendado)

### Pasos de instalación

1. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```

4. Crear datos de prueba:
   ```bash
   python manage.py seed_data
   ```

5. Ejecutar servidor:
   ```bash
   python manage.py runserver
   ```

La aplicación estará disponible en http://localhost:8000/

## Credenciales de Prueba

Después de ejecutar `python manage.py seed_data`, puedes usar:

- **Administrador:**
  - Email: admin@hundidos.local
  - Contraseña: admin123

- **Cliente:**
  - Email: cliente@hundidos.local
  - Contraseña: cliente123

## Estructura del Proyecto

- `accounts/` - Autenticación y gestión de usuarios
- `catalog/` - Catálogo de barcos, categorías, puertos y fabricantes
- `cart/` - Cesta de compra con persistencia en sesión
- `reservations/` - Gestión de reservas
- `payments/` - Procesamiento de pagos (PayPal y Contra Reembolso)
- `admin_panel/` - Panel de administración
- `core/` - Configuración central y utilidades
- `templates/` - Templates HTML
- `static/` - Archivos estáticos (CSS, JS, imágenes)

## Rutas Principales

- `/` - Página de inicio con catálogo
- `/barcos/` - Listado de barcos
- `/barcos/<id>/` - Detalle de barco
- `/accounts/registro/` - Registro de usuario
- `/accounts/login/` - Inicio de sesión
- `/accounts/logout/` - Cierre de sesión
- `/accounts/perfil/` - Perfil de usuario
- `/cesta/` - Cesta de compra
- `/reserva/paso1/` - Paso 1 de reserva
- `/reserva/paso2/` - Paso 2 de reserva
- `/reserva/paso3/` - Paso 3 de reserva
- `/admin/` - Panel de administración Django
- `/admin-panel/` - Panel de administración personalizado

## Docker

### Construcción de la imagen

```bash
docker build -t hundidos:latest .
```

### Ejecución del contenedor

```bash
docker run -p 8000:8000 hundidos:latest
```

La aplicación estará disponible en http://localhost:8000/

## Características Implementadas en Sprint 1

- ✅ Registro de cliente con validación de email
- ✅ Inicio de sesión con email y contraseña
- ✅ Cierre de sesión seguro
- ✅ Catálogo de barcos organizado por categorías
- ✅ Búsqueda y filtros combinables (nombre, categoría, puerto, fabricante, precio, capacidad, fechas)
- ✅ Ficha de barco con selección de cantidad
- ✅ Cesta de compra con persistencia en sesión
- ✅ Zona horaria Europe/Madrid y locale español
- ✅ Datos precargados (5 barcos, 2 puertos, 2 fabricantes, 2 categorías, usuarios de prueba)
- ✅ Dockerfile para empaquetado

## Próximos Pasos

- Implementar flujo de reserva en 3 pasos
- Integración con PayPal Sandbox
- Sistema de seguimiento de reservas
- Panel de administración personalizado
- Notificaciones por email
