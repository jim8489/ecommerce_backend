from rest_framework import serializers

from apps.products.serializers import ProductSerializer


class RecommendationSerializer(ProductSerializer):

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields