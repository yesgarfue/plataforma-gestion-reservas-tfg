# Hundidos - Alquiler de Barcos

Aplicación web monolítica de alquiler de barcos construida con Django 3.2, SQLite y PayPal Sandbox.

## Instalación

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

## Estructura del Proyecto

- `accounts/` - Autenticación y gestión de usuarios
- `catalog/` - Catálogo de barcos
- `cart/` - Cesta de compra
- `reservations/` - Gestión de reservas
- `payments/` - Procesamiento de pagos
- `admin_panel/` - Panel de administración
- `core/` - Configuración central y utilidades
