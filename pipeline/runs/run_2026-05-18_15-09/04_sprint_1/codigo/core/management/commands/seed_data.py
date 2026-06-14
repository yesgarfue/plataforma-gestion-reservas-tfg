from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import Categoria, Puerto, Fabricante, Barco


class Command(BaseCommand):
    help = 'Carga datos de prueba en la base de datos'

    def handle(self, *args, **options):
        # Crear categorías
        cat_velero, _ = Categoria.objects.get_or_create(
            nombre='Velero',
            defaults={'descripcion': 'Embarcaciones a vela'}
        )
        cat_motor, _ = Categoria.objects.get_or_create(
            nombre='Lancha Motora',
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
        fab_bavaria, _ = Fabricante.objects.get_or_create(
            nombre='Bavaria',
            defaults={'pais': 'Alemania'}
        )

        # Crear barcos
        barcos_data = [
            {
                'nombre': 'Vela Azul',
                'categoria': cat_velero,
                'puerto': puerto_barcelona,
                'fabricante': fab_beneteau,
                'precio_dia': 150.00,
                'capacidad': 6,
                'descripcion': 'Hermoso velero de 12 metros, ideal para navegación en el Mediterráneo.'
            },
            {
                'nombre': 'Vela Blanca',
                'categoria': cat_velero,
                'puerto': puerto_malaga,
                'fabricante': fab_bavaria,
                'precio_dia': 120.00,
                'capacidad': 4,
                'descripcion': 'Velero compacto perfecto para principiantes.'
            },
            {
                'nombre': 'Lancha Rápida',
                'categoria': cat_motor,
                'puerto': puerto_barcelona,
                'fabricante': fab_beneteau,
                'precio_dia': 200.00,
                'capacidad': 8,
                'descripcion': 'Lancha motora de alta velocidad con todas las comodidades.'
            },
            {
                'nombre': 'Lancha Confort',
                'categoria': cat_motor,
                'puerto': puerto_malaga,
                'fabricante': fab_bavaria,
                'precio_dia': 180.00,
                'capacidad': 6,
                'descripcion': 'Lancha motora con cabina y equipamiento completo.'
            },
            {
                'nombre': 'Vela Dorada',
                'categoria': cat_velero,
                'puerto': puerto_barcelona,
                'fabricante': fab_beneteau,
                'precio_dia': 160.00,
                'capacidad': 5,
                'descripcion': 'Velero de lujo con acabados premium.'
            },
        ]

        for barco_data in barcos_data:
            Barco.objects.get_or_create(
                nombre=barco_data['nombre'],
                defaults=barco_data
            )

        # Crear usuario administrador
        User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@hundidos.com',
                'is_staff': True,
                'is_superuser': True,
                'password': 'admin123'
            }
        )
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('admin123')
        admin_user.save()

        # Crear usuario cliente
        User.objects.get_or_create(
            username='cliente@hundidos.com',
            defaults={
                'email': 'cliente@hundidos.com',
                'is_staff': False,
                'is_superuser': False,
            }
        )
        cliente_user = User.objects.get(username='cliente@hundidos.com')
        cliente_user.set_password('cliente123')
        cliente_user.save()

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados exitosamente.'))
        self.stdout.write(self.style.SUCCESS('Usuario administrador: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('Usuario cliente: cliente@hundidos.com / cliente123'))
