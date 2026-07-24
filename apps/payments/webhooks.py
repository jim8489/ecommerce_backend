import stripe

from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import PaymentService


stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeWebhookView(APIView):

    authentication_classes = []

    permission_classes = []

    def post(
        self,
        request,
    ):

        payload = request.body

        signature = request.META.get(
            "HTTP_STRIPE_SIGNATURE"
        )

        try:

            event = stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET,
            )

        except (
            ValueError,
            stripe.error.SignatureVerificationError,
        ):

            return Response(
                {
                    "detail":
                    "Invalid webhook."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            event["type"]
            == "payment_intent.succeeded"
        ):

            payment_intent = (
                event["data"]["object"]
            )

            PaymentService.process_webhook(
                payment_intent["id"]
            )

        return Response(
            {
                "received": True
            },
            status=status.HTTP_200_OK,
        )