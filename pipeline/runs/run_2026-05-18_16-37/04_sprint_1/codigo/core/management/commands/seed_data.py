from django.core.management.base import BaseCommand
from catalog.models import Categoria, Puerto, Fabricante, Barco
from accounts.models import User

class Command(BaseCommand):
    help = 'Carga datos de ejemplo en la base de datos'

    def handle(self, *args, **options):
        # Crear categorías
        cat_velero, _ = Categoria.objects.get_or_create(
            nombre='Velero',
            defaults={'descripcion': 'Embarcaciones a vela'}
        )
        cat_motor, _ = Categoria.objects.get_or_create(
            nombre='Lancha motora',
            defaults={'descripcion': 'Embarcaciones con motor'}
        )

        # Crear puertos
        puerto_barcelona, _ = Puerto.objects.get_or_create(
            nombre='Barcelona',
            defaults={'ubicacion': 'Cataluña, España'}
        )
        puerto_malaga, _ = Puerto.objects.get_or_create(
            nombre='Málaga',
            defaults={'ubicacion': 'Andalucía, España'}
        )

        # Crear fabricantes
        fab_beneteau, _ = Fabricante.objects.get_or_create(
            nombre='Beneteau',
            defaults={'pais': 'Francia'}
        )
        fab_sunseeker, _ = Fabricante.objects.get_or_create(
            nombre='Sunseeker',
            defaults={'pais': 'Reino Unido'}
        )

        # Crear barcos
        barcos_data = [
            {
                'nombre': 'Vela Blanca',
                'categoria': cat_velero,
                'puerto': puerto_barcelona,
                'fabricante': fab_beneteau,
                'precio_dia': 150.00,
                'capacidad': 6,
                'descripcion': 'Hermoso velero de 12 metros',
                'disponible': True,
                'cantidad_disponible': 2,
            },
            {
                'nombre': 'Lancha Rápida',
                'categoria': cat_motor,
                'puerto': puerto_malaga,
                'fabricante': fab_sunseeker,
                'precio_dia': 200.00,
                'capacidad': 8,
                'descripcion': 'Lancha motora de lujo',
                'disponible': True,
                'cantidad_disponible': 1,
            },
            {
                'nombre': 'Velero Clásico',
                'categoria': cat_velero,
                'puerto': puerto_barcelona,
                'fabricante': fab_beneteau,
                'precio_dia': 120.00,
                'capacidad': 4,
                'descripcion': 'Velero tradicional de 10 metros',
                'disponible': True,
                'cantidad_disponible': 3,
            },
            {
                'nombre': 'Crucero de Lujo',
                'categoria': cat_motor,
                'puerto': puerto_malaga,
                'fabricante': fab_sunseeker,
                'precio_dia': 300.00,
                'capacidad': 12,
                'descripcion': 'Crucero de lujo con todas las comodidades',
                'disponible': True,
                'cantidad_disponible': 1,
            },
            {
                'nombre': 'Velero Deportivo',
                'categoria': cat_velero,
                'puerto': puerto_barcelona,
                'fabricante': fab_beneteau,
                'precio_dia': 180.00,
                'capacidad': 5,
                'descripcion': 'Velero deportivo de competición',
                'disponible': True,
                'cantidad_disponible': 2,
            },
        ]

        for barco_data in barcos_data:
            Barco.objects.get_or_create(
                nombre=barco_data['nombre'],
                defaults=barco_data
            )

        # Crear usuario administrador
        User.objects.get_or_create(
            email='admin@hundidos.com',
            defaults={
                'nombre': 'Administrador',
                'es_administrador': True,
                'password': 'pbkdf2_sha256$260000$abcdefghijklmnopqrst$1234567890abcdefghijklmnopqrstuvwxyz',
            }
        )
        admin_user = User.objects.get(email='admin@hundidos.com')
        admin_user.set_password('admin123')
        admin_user.save()

        # Crear usuario cliente
        User.objects.get_or_create(
            email='cliente@hundidos.com',
            defaults={
                'nombre': 'Cliente de Prueba',
                'es_administrador': False,
                'password': 'pbkdf2_sha256$260000$abcdefghijklmnopqrst$1234567890abcdefghijklmnopqrstuvwxyz',
            }
        )
        client_user = User.objects.get(email='cliente@hundidos.com')
        client_user.set_password('cliente123')
        client_user.save()

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo cargados correctamente.'))
        self.stdout.write(self.style.SUCCESS('Usuario administrador: admin@hundidos.com / admin123'))
        self.stdout.write(self.style.SUCCESS('Usuario cliente: cliente@hundidos.com / cliente123'))
