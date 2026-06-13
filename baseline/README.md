# Hundidos - Baseline humano

Aplicacion web Django para el alquiler de barcos desarrollada por el equipo
humano. Este proyecto constituye el baseline del estudio comparativo frente al
producto obtenido mediante el pipeline hibrido humano-IA.

## Requisitos

- Python 3.10 o 3.11
- `pip`

## Instalacion

Desde la carpeta `baseline`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Opcionalmente, copia el archivo de ejemplo para personalizar la configuracion
local:

```powershell
Copy-Item .env.example .env
```

El archivo `.env` es local y no se incluye en Git. Para una ejecucion de
desarrollo se pueden conservar los valores del ejemplo; en otros entornos debe
usarse una `SECRET_KEY` propia.

En Linux o macOS, la activacion del entorno es:

```bash
source .venv/bin/activate
```

## Preparacion de la base de datos

La base de datos local `db.sqlite3` no se incluye en el repositorio. Para crear
una base limpia con datos sinteticos de demostracion:

```powershell
python manage.py migrate
python manage.py seed_demo
```

El comando `seed_demo` es idempotente: puede ejecutarse varias veces sin
duplicar los datos principales.

Los datos creados incluyen:

- una cuenta administradora;
- una cuenta de cliente;
- categorias de embarcaciones;
- puertos y fabricantes;
- cuatro barcos de demostracion.

## Ejecucion

```powershell
python manage.py runserver
```

La aplicacion queda disponible en:

```text
http://127.0.0.1:8000/
```

Rutas principales:

- Catalogo: `http://127.0.0.1:8000/store/`
- Login: `http://127.0.0.1:8000/accounts/login/`
- Panel de reservas: `http://127.0.0.1:8000/orders/reservas/`
- Administracion Django: `http://127.0.0.1:8000/securelogin/`

## Credenciales de demostracion

Administrador:

```text
Email: admin@admin.com
Contrasena: admin
```

Cliente:

```text
Email: pedro@pedro.com
Contrasena: Pedro1234!
```

Estas credenciales son exclusivamente sinteticas y se crean mediante
`seed_demo`.

## Correo electronico

El proyecto utiliza el backend de consola de Django. Los mensajes de
activacion, recuperacion de contrasena y confirmacion se muestran en la
terminal donde se ejecuta el servidor; no se envian correos reales.

## Archivos no incluidos

- `db.sqlite3`: base local recreable mediante migraciones y `seed_demo`.
- `.venv/` y `venv/`: entornos virtuales locales.
- `static/`: salida generada por `collectstatic`.
- `media/userprofile/`: imagenes subidas por usuarios.

Los archivos fuente de estilos y JavaScript se conservan en
`ecommerce/static/`. Las imagenes necesarias para los barcos demo se conservan
en `media/images/barcos/`.

Para generar los archivos estaticos de despliegue:

```powershell
python manage.py collectstatic --noinput
```
