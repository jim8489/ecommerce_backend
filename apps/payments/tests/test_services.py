from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payments.services import PaymentService


User = get_user_model()


class PaymentServiceTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
        )

        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("100.00"),
        )

    @patch("apps.payments.factory.PaymentFactory.get")
    def test_initiate_payment(self, mock_factory):

        strategy = mock_factory.return_value

        strategy.initiate_payment.return_value = {
            "transaction_id": "pi_test",
            "client_secret": "secret",
            "raw_response": {},
        }

        result = PaymentService.initiate_payment(
            self.order.id,
            Payment.Provider.STRIPE,
        )

        self.assertEqual(
            result["payment"].transaction_id,
            "pi_test",
        )

        self.assertEqual(
            result["client_secret"],
            "secret",
        )