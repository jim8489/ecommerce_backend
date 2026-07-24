from rest_framework.test import APITestCase
from rest_framework import status


class AuthenticationTests(
    APITestCase
):

    def test_register(self):

        response = self.client.post(
            "/api/auth/register/",
            {
                "email": "john@example.com",
                "password": "Password@123",
                "first_name": "John",
                "last_name": "Doe",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )