from django.db import models

from apps.orders.models import Order


class Payment(models.Model):

    class Provider(models.TextChoices):
        STRIPE = "STRIPE", "Stripe"
        BKASH = "BKASH", "bKash"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    provider = models.CharField(
        max_length=20,
        choices=Provider.choices,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    transaction_id = models.CharField(
        max_length=255,
        unique=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    raw_response = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "payments"

        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(fields=["provider"]),
            models.Index(fields=["status"]),
            models.Index(fields=["transaction_id"]),
        ]

    def __str__(self):
        return (
            f"{self.provider} - "
            f"{self.transaction_id}"
        )