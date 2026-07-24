from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.products.models import (
    Category,
    Product,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Seed initial data"

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.SUCCESS(
                "\nSeeding database...\n"
            )
        )

        admin, created = (
            User.objects.get_or_create(
                email="admin@example.com",
                defaults={
                    "is_staff": True,
                    "is_superuser": True,
                },
            )
        )

        if created:
            admin.set_password("admin123")
            admin.save()

        user, created = (
            User.objects.get_or_create(
                email="user@example.com",
            )
        )

        if created:
            user.set_password("user123")
            user.save()

        electronics, _ = (
            Category.objects.get_or_create(
                name="Electronics",
            )
        )

        laptops, _ = (
            Category.objects.get_or_create(
                name="Laptops",
                parent=electronics,
            )
        )

        gaming, _ = (
            Category.objects.get_or_create(
                name="Gaming Laptops",
                parent=laptops,
            )
        )

        phones, _ = (
            Category.objects.get_or_create(
                name="Phones",
                parent=electronics,
            )
        )

        Product.objects.get_or_create(
            sku="TV001",
            defaults={
                "category": electronics,
                "name": "Smart TV",
                "description": "55 inch Smart TV",
                "price": Decimal("900.00"),
                "stock": 10,
                "status": Product.Status.ACTIVE,
            },
        )

        Product.objects.get_or_create(
            sku="LP001",
            defaults={
                "category": laptops,
                "name": "Ultrabook",
                "description": "Lightweight Laptop",
                "price": Decimal("1400.00"),
                "stock": 15,
                "status": Product.Status.ACTIVE,
            },
        )

        Product.objects.get_or_create(
            sku="GL001",
            defaults={
                "category": gaming,
                "name": "Gaming Laptop",
                "description": "RTX Gaming Laptop",
                "price": Decimal("2200.00"),
                "stock": 8,
                "status": Product.Status.ACTIVE,
            },
        )

        Product.objects.get_or_create(
            sku="PH001",
            defaults={
                "category": phones,
                "name": "Smart Phone",
                "description": "Android Flagship",
                "price": Decimal("850.00"),
                "stock": 20,
                "status": Product.Status.ACTIVE,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Database seeded successfully."
            )
        )