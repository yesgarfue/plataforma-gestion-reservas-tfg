from django.core.management.base import BaseCommand

from accounts.models import Account, UserProfile
from category.models import Category
from store.models import Fabricante, Product, Puerto


class Command(BaseCommand):
    help = "Crea los usuarios y datos sinteticos necesarios para la demostracion."

    def handle(self, *args, **options):
        admin = self._crear_usuario(
            email="admin@admin.com",
            username="admin",
            password="admin",
            first_name="Admin",
            last_name="Demo",
            phone_number="600000001",
            is_admin=True,
        )
        cliente = self._crear_usuario(
            email="pedro@pedro.com",
            username="pedro",
            password="Pedro1234!",
            first_name="Pedro",
            last_name="Demo",
            phone_number="600000002",
            is_admin=False,
        )

        for user in (admin, cliente):
            UserProfile.objects.get_or_create(user=user)

        categorias = {
            "veleros": Category.objects.update_or_create(
                slug="veleros",
                defaults={
                    "category_name": "Veleros",
                    "description": "Veleros disponibles para alquiler.",
                },
            )[0],
            "barcos-motor": Category.objects.update_or_create(
                slug="barcos-motor",
                defaults={
                    "category_name": "Barcos a motor",
                    "description": "Barcos a motor disponibles para alquiler.",
                },
            )[0],
            "catamaranes": Category.objects.update_or_create(
                slug="catamaranes",
                defaults={
                    "category_name": "Catamaranes",
                    "description": "Catamaranes disponibles para alquiler.",
                },
            )[0],
        }

        puertos = {
            nombre: Puerto.objects.get_or_create(nombre=nombre)[0]
            for nombre in ("Santa Maria", "Barbate", "Tarifa", "Bahia de Cadiz")
        }
        fabricantes = {
            nombre: Fabricante.objects.get_or_create(nombre=nombre)[0]
            for nombre in ("Rodman", "Beneteau", "Jeanneau")
        }

        barcos = [
            {
                "product_name": "Velero Esperanza",
                "description": "Velero de demostracion para navegar por la costa.",
                "price": 50,
                "images": "images/barcos/1.jpg",
                "stock": 2,
                "category": categorias["veleros"],
                "fabricante": fabricantes["Rodman"],
                "puerto": puertos["Santa Maria"],
                "capacidad": 2,
            },
            {
                "product_name": "Lancha Trueno",
                "description": "Lancha rapida para excursiones costeras.",
                "price": 65,
                "images": "images/barcos/2.jpg",
                "stock": 4,
                "category": categorias["barcos-motor"],
                "fabricante": fabricantes["Jeanneau"],
                "puerto": puertos["Barbate"],
                "capacidad": 4,
            },
            {
                "product_name": "Catamaran Azul",
                "description": "Catamaran amplio para grupos y familias.",
                "price": 120,
                "images": "images/barcos/3.jpg",
                "stock": 3,
                "category": categorias["catamaranes"],
                "fabricante": fabricantes["Beneteau"],
                "puerto": puertos["Tarifa"],
                "capacidad": 8,
            },
            {
                "product_name": "Yate Bahia",
                "description": "Yate de demostracion con capacidad para seis personas.",
                "price": 180,
                "images": "images/barcos/4.jpg",
                "stock": 2,
                "category": categorias["barcos-motor"],
                "fabricante": fabricantes["Rodman"],
                "puerto": puertos["Bahia de Cadiz"],
                "capacidad": 6,
            },
        ]

        for datos in barcos:
            Product.objects.update_or_create(
                product_name=datos["product_name"],
                defaults={
                    **datos,
                    "is_available": True,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Datos demo creados: 2 usuarios, 3 categorias, "
                "4 puertos, 3 fabricantes y 4 barcos."
            )
        )

    def _crear_usuario(
        self,
        *,
        email,
        username,
        password,
        first_name,
        last_name,
        phone_number,
        is_admin,
    ):
        user, _ = Account.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
            },
        )
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.is_active = True
        user.is_admin = is_admin
        user.is_staff = is_admin
        user.is_superadmin = is_admin
        user.set_password(password)
        user.save()
        return user
