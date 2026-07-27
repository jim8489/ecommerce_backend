from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Category, Product


class ProductAPITest(APITestCase):

    def setUp(self):

        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

        Product.objects.create(
            category=self.category,
            name="Laptop",
            sku="LAP001",
            description="Gaming Laptop",
            price=Decimal("500.00"),
            stock=20,
            status="ACTIVE",
        )

    def test_list_products(self):

        response = self.client.get(
            reverse("products-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_product_detail(self):

        product = Product.objects.first()

        response = self.client.get(
            reverse(
                "products-detail",
                args=[product.id],
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )