from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User


class AuthenticationAPITest(APITestCase):

    def test_register_user(self):

        data = {
            "email": "john@example.com",
            "password": "Password123!",
            "first_name": "John",
            "last_name": "Doe",
        }

        response = self.client.post(
            reverse("register"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                email="john@example.com"
            ).exists()
        )

    def test_login_user(self):

        User.objects.create_user(
            email="john@example.com",
            password="Password123!",
            first_name="John",
            last_name="Doe",
        )

        response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "email": "john@example.com",
                "password": "Password123!",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)