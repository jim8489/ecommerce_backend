from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError

from apps.orders.models import Order

from .factory import PaymentFactory
from .models import Payment


class PaymentService:
    """
    Handles payment initiation,
    verification and webhook processing.
    """

    @staticmethod
    @transaction.atomic
    def initiate_payment(order_id, provider):
        """
        Create a pending payment and
        initiate the selected provider.
        """

        order = get_object_or_404(
            Order.objects.select_for_update().prefetch_related(
                "items",
                "items__product",
            ),
            pk=order_id,
        )

        if order.status == Order.Status.PAID:
            raise ValidationError(
                "This order has already been paid."
            )

        if hasattr(order, "payment"):
            raise ValidationError(
                "Payment already exists for this order."
            )

        strategy = PaymentFactory.get(provider)

        response = strategy.initiate_payment(order)

        payment = Payment.objects.create(
            order=order,
            provider=provider,
            amount=order.total_amount,
            transaction_id=response["transaction_id"],
            status=Payment.Status.PENDING,
            raw_response=response["raw_response"],
        )

        return {
            "payment": payment,
            "client_secret": response["client_secret"],
        }

    @staticmethod
    @transaction.atomic
    def confirm_payment(transaction_id):
        """
        Verify payment, update payment,
        mark order as paid and reduce stock.
        """

        payment = get_object_or_404(
            Payment.objects.select_related("order").prefetch_related(
                "order__items",
                "order__items__product",
            ),
            transaction_id=transaction_id,
        )

        if payment.status == Payment.Status.SUCCESS:
            return payment

        strategy = PaymentFactory.get(
            payment.provider
        )

        verification = strategy.verify_payment(
            payment.transaction_id
        )

        if verification["status"] != "SUCCESS":

            payment.status = Payment.Status.FAILED
            payment.raw_response = verification

            payment.save(
                update_fields=[
                    "status",
                    "raw_response",
                ]
            )

            raise ValidationError(
                "Payment verification failed."
            )

        order = payment.order

        for item in order.items.all():

            product = item.product

            if product.stock < item.quantity:

                raise ValidationError(
                    f"Insufficient stock for {product.name}"
                )

            product.stock -= item.quantity

            product.save(
                update_fields=[
                    "stock",
                ]
            )

        payment.status = Payment.Status.SUCCESS
        payment.raw_response = verification

        payment.save(
            update_fields=[
                "status",
                "raw_response",
            ]
        )

        order.status = Order.Status.PAID

        order.save(
            update_fields=[
                "status",
            ]
        )

        return payment

    @staticmethod
    @transaction.atomic
    def process_webhook(transaction_id):
        """
        Process payment confirmation
        received from Stripe or bKash.
        """

        return PaymentService.confirm_payment(
            transaction_id
        )