import stripe

from django.conf import settings

from .base import PaymentStrategy


stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeStrategy(PaymentStrategy):
    """
    Stripe Payment Intent Strategy.
    """

    def initiate_payment(
        self,
        order,
    ):

        intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),
            currency="usd",
            metadata={
                "order_id": str(order.id),
            },
            automatic_payment_methods={
                "enabled": True,
            },
        )

        return {
            "transaction_id": intent.id,
            "client_secret": intent.client_secret,
            "status": intent.status,
            "raw_response": intent.to_dict(),
        }

    def verify_payment(
        self,
        transaction_id,
    ):

        intent = stripe.PaymentIntent.retrieve(
            transaction_id
        )

        if intent.status == "succeeded":

            payment_status = "SUCCESS"

        elif intent.status in [
            "processing",
            "requires_capture",
            "requires_action",
            "requires_confirmation",
        ]:

            payment_status = "PENDING"

        else:

            payment_status = "FAILED"

        return {
            "transaction_id": intent.id,
            "status": payment_status,
            "raw_response": intent.to_dict(),
        }