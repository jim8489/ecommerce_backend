from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product

User = get_user_model()


class ProductAPITest(APITestCase):

    def setUp(self):

        self.admin = User.objects.create_user(
            email="admin@test.com",
            password="admin123",
            is_staff=True,
        )

        self.user = User.objects.create_user(
            email="user@test.com",
            password="user123",
        )

        self.category = Category.objects.create(
            name="Electronics",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            sku="LAP001",
            description="Gaming Laptop",
            price=Decimal("1200.00"),
            stock=10,
        )

    def test_product_list(self):

        self.client.force_authenticate(
            self.user
        )

        response = self.client.get(
            "/api/products/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_admin_create_product(self):

        self.client.force_authenticate(
            self.admin
        )

        data = {
            "category": self.category.id,
            "name": "Mouse",
            "sku": "M001",
            "description": "Wireless Mouse",
            "price": "40.00",
            "stock": 15,
            "status": "ACTIVE",
        }

        response = self.client.post(
            "/api/products/",
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_normal_user_cannot_create_product(self):

        self.client.force_authenticate(
            self.user
        )

        data = {
            "category": self.category.id,
            "name": "Keyboard",
            "sku": "K001",
            "description": "Mechanical",
            "price": "90.00",
            "stock": 5,
            "status": "ACTIVE",
        }

        response = self.client.post(
            "/api/products/",
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_search_product(self):

        self.client.force_authenticate(
            self.user
        )

        response = self.client.get(
            "/api/products/?search=Laptop"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_filter_product(self):

        self.client.force_authenticate(
            self.user
        )

        response = self.client.get(
            "/api/products/?status=ACTIVE"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        
#category tests
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product
from .services import ProductService

User = get_user_model()


class CategoryAPITest(APITestCase):

    def setUp(self):

        self.admin = User.objects.create_user(
            email="admin@test.com",
            password="admin123",
            is_staff=True,
        )

        self.user = User.objects.create_user(
            email="user@test.com",
            password="user123",
        )

        self.root = Category.objects.create(
            name="Electronics"
        )

        self.child = Category.objects.create(
            name="Laptop",
            parent=self.root,
        )

        self.grandchild = Category.objects.create(
            name="Gaming",
            parent=self.child,
        )

    def test_category_list(self):

        self.client.force_authenticate(
            self.user
        )

        response = self.client.get(
            "/api/categories/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_admin_create_category(self):

        self.client.force_authenticate(
            self.admin
        )

        response = self.client.post(
            "/api/categories/",
            {
                "name": "Phone"
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_normal_user_cannot_create_category(self):

        self.client.force_authenticate(
            self.user
        )

        response = self.client.post(
            "/api/categories/",
            {
                "name": "Tablet"
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_category_tree_cached(self):

        cache.clear()

        ProductService.get_category_tree()

        self.assertIsNotNone(
            cache.get("category_tree")
        )

    def test_cache_invalidated(self):

        cache.clear()

        ProductService.get_category_tree()

        self.assertIsNotNone(
            cache.get("category_tree")
        )

        cache.delete("category_tree")

        self.assertIsNone(
            cache.get("category_tree")
        )
        
##recomendation tests
class RecommendationAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="user@test.com",
            password="user123",
        )

        self.root = Category.objects.create(
            name="Electronics"
        )

        self.child = Category.objects.create(
            name="Laptop",
            parent=self.root,
        )

        self.grandchild = Category.objects.create(
            name="Gaming",
            parent=self.child,
        )

        self.root_product = Product.objects.create(
            category=self.root,
            name="TV",
            sku="TV001",
            description="Smart TV",
            price=Decimal("1000.00"),
            stock=5,
        )

        self.child_product = Product.objects.create(
            category=self.child,
            name="Ultrabook",
            sku="LP001",
            description="Laptop",
            price=Decimal("1200.00"),
            stock=10,
        )

        self.grandchild_product = Product.objects.create(
            category=self.grandchild,
            name="Gaming Laptop",
            sku="GL001",
            description="Gaming",
            price=Decimal("1800.00"),
            stock=7,
        )

    def test_related_products_include_descendants(self):

        products = ProductService.get_related_products(
            self.root.id
        )

        ids = list(
            products.values_list(
                "id",
                flat=True,
            )
        )

        self.assertIn(
            self.root_product.id,
            ids,
        )

        self.assertIn(
            self.child_product.id,
            ids,
        )

        self.assertIn(
            self.grandchild_product.id,
            ids,
        )

    def test_related_products_exclude_current(self):

        products = ProductService.get_related_products(
            self.root.id,
            exclude_product_id=self.root_product.id,
        )

        ids = list(
            products.values_list(
                "id",
                flat=True,
            )
        )

        self.assertNotIn(
            self.root_product.id,
            ids,
        )

    def test_leaf_category_returns_only_leaf_products(self):

        products = ProductService.get_related_products(
            self.grandchild.id
        )

        ids = list(
            products.values_list(
                "id",
                flat=True,
            )
        )

        self.assertEqual(
            ids,
            [self.grandchild_product.id],
        )