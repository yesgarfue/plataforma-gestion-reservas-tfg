from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import Categoria, Puerto, Fabricante, Barco
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Carga datos de prueba en la base de datos'

    def handle(self, *args, **options):
        # Crear categorías
        categorias_data = [
            {'nombre': 'Velero', 'descripcion': 'Barcos de vela'},
            {'nombre': 'Lancha', 'descripcion': 'Lanchas motorizadas'},
        ]
        categorias = {}
        for cat_data in categorias_data:
            cat, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            categorias[cat_data['nombre']] = cat
            if created:
                self.stdout.write(f'Categoría creada: {cat.nombre}')

        # Crear puertos
        puertos_data = [
            {'nombre': 'Puerto de Barcelona', 'ubicacion': 'Barcelona, España'},
            {'nombre': 'Puerto de Palma', 'ubicacion': 'Palma de Mallorca, España'},
        ]
        puertos = {}
        for puerto_data in puertos_data:
            puerto, created = Puerto.objects.get_or_create(
                nombre=puerto_data['nombre'],
                defaults={'ubicacion': puerto_data['ubicacion']}
            )
            puertos[puerto_data['nombre']] = puerto
            if created:
                self.stdout.write(f'Puerto creado: {puerto.nombre}')

        # Crear fabricantes
        fabricantes_data = [
            {'nombre': 'Beneteau', 'pais': 'Francia'},
            {'nombre': 'Jeanneau', 'pais': 'Francia'},
        ]
        fabricantes = {}
        for fab_data in fabricantes_data:
            fab, created = Fabricante.objects.get_or_create(
                nombre=fab_data['nombre'],
                defaults={'pais': fab_data['pais']}
            )
            fabricantes[fab_data['nombre']] = fab
            if created:
                self.stdout.write(f'Fabricante creado: {fab.nombre}')

        # Crear barcos
        barcos_data = [
            {
                'nombre': 'Velero Azul',
                'categoria': 'Velero',
                'puerto': 'Puerto de Barcelona',
                'fabricante': 'Beneteau',
                'precio_dia': 150.00,
                'capacidad': 6,
                'disponibilidad': 2,
            },
            {
                'nombre': 'Velero Blanco',
                'categoria': 'Velero',
                'puerto': 'Puerto de Palma',
                'fabricante': 'Jeanneau',
                'precio_dia': 180.00,
                'capacidad': 8,
                'disponibilidad': 1,
            },
            {
                'nombre': 'Lancha Rápida',
                'categoria': 'Lancha',
                'puerto': 'Puerto de Barcelona',
                'fabricante': 'Beneteau',
                'precio_dia': 200.00,
                'capacidad': 4,
                'disponibilidad': 3,
            },
            {
                'nombre': 'Lancha Deportiva',
                'categoria': 'Lancha',
                'puerto': 'Puerto de Palma',
                'fabricante': 'Jeanneau',
                'precio_dia': 220.00,
                'capacidad': 5,
                'disponibilidad': 2,
            },
            {
                'nombre': 'Velero Clásico',
                'categoria': 'Velero',
                'puerto': 'Puerto de Barcelona',
                'fabricante': 'Beneteau',
                'precio_dia': 160.00,
                'capacidad': 7,
                'disponibilidad': 1,
            },
        ]
        for barco_data in barcos_data:
            barco, created = Barco.objects.get_or_create(
                nombre=barco_data['nombre'],
                defaults={
                    'categoria': categorias[barco_data['categoria']],
                    'puerto': puertos[barco_data['puerto']],
                    'fabricante': fabricantes[barco_data['fabricante']],
                    'precio_dia': barco_data['precio_dia'],
                    'capacidad': barco_data['capacidad'],
                    'disponibilidad': barco_data['disponibilidad'],
                    'activo': True,
                }
            )
            if created:
                self.stdout.write(f'Barco creado: {barco.nombre}')

        # Crear usuario administrador
        admin_user, created = User.objects.get_or_create(
            username='admin@hundidos.local',
            defaults={
                'email': 'admin@hundidos.local',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            UserProfile.objects.get_or_create(user=admin_user)
            self.stdout.write(f'Usuario administrador creado: admin@hundidos.local / admin123')

        # Crear usuario cliente
        client_user, created = User.objects.get_or_create(
            username='cliente@hundidos.local',
            defaults={
                'email': 'cliente@hundidos.local',
                'is_staff': False,
                'is_superuser': False,
            }
        )
        if created:
            client_user.set_password('cliente123')
            client_user.save()
            UserProfile.objects.get_or_create(user=client_user)
            self.stdout.write(f'Usuario cliente creado: cliente@hundidos.local / cliente123')

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados correctamente.'))
