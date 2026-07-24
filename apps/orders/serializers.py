from decimal import Decimal

from rest_framework import serializers

from .models import Order, OrderItem
from apps.products.models import Product


class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:
        model = OrderItem

        fields = (
            "id",
            "product",
            "product_name",
            "quantity",
            "price",
            "subtotal",
        )


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order

        fields = (
            "id",
            "user",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
            "items",
        )

        read_only_fields = (
            "id",
            "user",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        )


class CreateOrderSerializer(serializers.Serializer):

    items = OrderItemCreateSerializer(
        many=True
    )

    def validate_items(self, value):

        if not value:
            raise serializers.ValidationError(
                "Order must contain at least one product."
            )

        return value