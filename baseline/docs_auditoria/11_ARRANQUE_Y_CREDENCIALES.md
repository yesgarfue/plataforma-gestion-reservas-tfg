# 11 — Arranque y Credenciales

[← Volver al índice](00_INDICE.md)

---

## Prerrequisitos

- Python 3.8+ (el Dockerfile usa 3.8.10; versiones más nuevas también deberían funcionar)
- pip
- (Opcional) virtualenv o venv

---

## Pasos para arrancar el proyecto localmente

### 1. Clonar / situarse en el directorio

```bash
cd "d:/University/TFG/Trabajo Fin Grado/02_Experimentos_código/CodigoBase/PGPI-G3.2/Django/hundidos"
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> **Nota:** `playwright` y `selenium` son pesados y requieren navegadores adicionales. Si solo quieres ejecutar la app (sin tests), puedes instalar sin ellos:
> ```bash
> pip install -r requirements.txt --ignore-requires-python
> ```
> O editar `requirements.txt` para eliminar esas dos líneas antes de instalar.

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

El archivo `db.sqlite3` ya está en el repositorio con datos de prueba. Si quieres empezar desde cero, elimínalo antes de ejecutar `migrate`.

### 5. Recolectar estáticos (opcional, solo necesario si sirves con gunicorn/nginx)

```bash
python manage.py collectstatic --noinput
```

### 6. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en `http://127.0.0.1:8000/`.

---

## Arranque con Docker

```bash
# Construir imagen y levantar
docker-compose up --build

# El servidor estará disponible en http://localhost:8000
```

> **Advertencia:** El `Dockerfile` ejecuta `makemigrations && migrate && runserver` en el CMD — esto NO es apropiado para producción. Es solo para desarrollo.

---

## Credenciales y datos de acceso encontrados

### Cuenta de email del sistema

| Campo | Valor |
|---|---|
| Email | `hundidosgestion@gmail.com` |
| Contraseña de aplicación | Credencial retirada del repositorio; debe rotarse |

Esta cuenta se usa para enviar todos los emails del sistema (verificación, recuperación de contraseña, confirmación de reserva). Ver `ecommerce/settings.py:31-32`.

> ⚠️ **Esta credencial debería rotarse.** Está expuesta en el repositorio. Para revocarla: acceder a la cuenta de Google → Seguridad → Contraseñas de aplicación → eliminar la existente y generar una nueva.

### Panel de administración Django

La URL del admin está ofuscada: **`/securelogin/`** (en lugar del estándar `/admin/`). Ver `ecommerce/urls.py:24`.

No se pueden determinar las credenciales de superusuario sin acceder directamente a `db.sqlite3`. El archivo de base de datos está en el repositorio; para ver los usuarios:

```bash
# Opción A: desde Django shell
python manage.py shell
>>> from accounts.models import Account
>>> Account.objects.filter(is_superadmin=True).values('email', 'is_active', 'is_admin')
```

```bash
# Opción B: DB Browser for SQLite
# Abrir db.sqlite3 → tabla accounts_account → ver registros con is_superadmin=1
```

### Cuenta PayPal de negocio

La cuenta PayPal vinculada tiene el client-id `AcR7zkdXWRgqllj3uJaMWfNl3hsmA0dOkpP-nu2I7cFtKxaeTJFFfV2IeadmHtCkwSNwQwt3xwZzJ2jQ` (visible en `templates/base.html:33`). No es una credencial secreta en el sentido técnico, pero identifica la cuenta de negocio receptora de pagos.

---

## Cómo crear un superusuario nuevo

Si no encuentras las credenciales de admin o quieres crear un usuario desde cero:

```bash
python manage.py createsuperuser
```

Django solicitará:
- `first_name` y `last_name` (campos requeridos del modelo personalizado)
- `email` (campo de login)
- `username`
- `password` (debe cumplir `CustomPasswordValidator`: ≥8 chars, mayúscula, minúscula, número, carácter especial)

Tras crear el superusuario, acceder a `http://127.0.0.1:8000/securelogin/`.

---

## Variables de entorno necesarias para producción

Si en algún momento se migra a un esquema de variables de entorno (lo cual es **altamente recomendable**), estas son las variables mínimas:

```env
SECRET_KEY=<cadena-aleatoria-50-caracteres>
DEBUG=False
EMAIL_HOST_PASSWORD=<contraseña-de-aplicacion-gmail>
PAYPAL_CLIENT_ID=<client-id-paypal>
DATABASE_URL=<si-se-migra-a-postgresql>
```

---

[← Volver al índice](00_INDICE.md)
