from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.orders.models import Order


User = get_user_model()


class PaymentApiTest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
        )

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("100.00"),
        )

    def test_payment_list(self):

        response = self.client.get(
            "/api/payments/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )