from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient


class StripeWebhookTest(TestCase):

    def setUp(self):

        self.client = APIClient()

    @patch(
        "apps.payments.webhooks.PaymentService.process_webhook"
    )
    @patch(
        "apps.payments.webhooks.stripe.Webhook.construct_event"
    )
    def test_webhook(
        self,
        mock_construct_event,
        mock_process,
    ):

        mock_construct_event.return_value = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_test_123"
                }
            },
        }

        response = self.client.post(
            "/api/payments/stripe/webhook/",
            data=b'{}',
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test_signature",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        mock_construct_event.assert_called_once()

        mock_process.assert_called_once_with(
            "pi_test_123"
        )