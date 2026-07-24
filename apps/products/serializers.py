from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "parent",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "slug",
            "created_at",
            "updated_at",
        )


class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "category_name",
            "name",
            "sku",
            "description",
            "price",
            "stock",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "sku",
            "created_at",
            "updated_at",
        )

    def validate_price(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )

        return value

    def validate_stock(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Stock cannot be negative."
            )

        return value