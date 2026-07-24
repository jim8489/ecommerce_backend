from rest_framework import serializers

from .models import Payment


class PaymentInitiateSerializer(serializers.Serializer):

    order_id = serializers.IntegerField()

    provider = serializers.ChoiceField(
        choices=Payment.Provider.choices,
    )


class PaymentConfirmSerializer(serializers.Serializer):

    transaction_id = serializers.CharField(
        max_length=255,
    )


class PaymentSerializer(serializers.ModelSerializer):

    order_id = serializers.IntegerField(
        source="order.id",
        read_only=True,
    )

    class Meta:

        model = Payment

        fields = (
            "id",
            "order_id",
            "provider",
            "amount",
            "transaction_id",
            "status",
            "raw_response",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields