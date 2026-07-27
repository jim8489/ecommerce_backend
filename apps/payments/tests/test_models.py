from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.orders.models import Order
from apps.payments.models import Payment


User = get_user_model()


class PaymentModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
        )

        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal("100.00"),
        )

    def test_create_payment(self):

        payment = Payment.objects.create(
            order=self.order,
            provider=Payment.Provider.STRIPE,
            amount=Decimal("100.00"),
            transaction_id="pi_test123",
        )

        self.assertEqual(
            payment.provider,
            Payment.Provider.STRIPE,
        )

        self.assertEqual(
            payment.status,
            Payment.Status.PENDING,
        )

        self.assertEqual(
            str(payment),
            "STRIPE - pi_test123",
        )