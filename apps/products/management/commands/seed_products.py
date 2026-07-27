from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.products.models import Category, Product


class Command(BaseCommand):
    help = "Seed sample products"


    def handle(self, *args, **kwargs):

        electronics, _ = Category.objects.get_or_create(
            name="Electronics",
            slug="electronics",
        )

        products = [

            {
                "name": "MacBook Air M1",
                "sku": "MAC001",
                "price": Decimal("899.99"),
                "stock": 15,
            },

            {
                "name": "iPhone 15",
                "sku": "IPH001",
                "price": Decimal("999.99"),
                "stock": 25,
            },

            {
                "name": "Samsung S24",
                "sku": "SAM001",
                "price": Decimal("849.99"),
                "stock": 18,
            },

            {
                "name": "AirPods Pro",
                "sku": "AIR001",
                "price": Decimal("249.99"),
                "stock": 40,
            },

            {
                "name": "Mechanical Keyboard",
                "sku": "KEY001",
                "price": Decimal("129.99"),
                "stock": 50,
            },

        ]

        for item in products:

            Product.objects.get_or_create(
                sku=item["sku"],
                defaults={
                    "category": electronics,
                    "name": item["name"],
                    "description": item["name"],
                    "price": item["price"],
                    "stock": item["stock"],
                    "status": Product.Status.ACTIVE,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Products seeded successfully."
            )
        )