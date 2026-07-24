from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .cache import invalidate_category_cache
from .filters import ProductFilter
from .models import Category, Product
from .pagination import ProductPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    ProductSerializer,
)
from .services import ProductService


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer

    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):

        serializer.save()

        invalidate_category_cache()

    def perform_update(self, serializer):

        serializer.save()

        invalidate_category_cache()

    def perform_destroy(self, instance):

        instance.delete()

        invalidate_category_cache()


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.select_related(
        "category"
    )

    serializer_class = ProductSerializer

    permission_classes = [IsAdminOrReadOnly]

    pagination_class = ProductPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ProductFilter

    search_fields = [
        "name",
        "sku",
        "description",
    ]

    ordering_fields = [
        "price",
        "created_at",
        "stock",
    ]

    def perform_create(self, serializer):

        serializer.save()

    def perform_update(self, serializer):

        serializer.save()

    def perform_destroy(self, instance):

        ProductService.delete_product(
            instance
        )


class RelatedProductsView(APIView):
    """
    Recommend products using DFS traversal
    of the category hierarchy.
    """

    permission_classes = [AllowAny]

    def get(
        self,
        request,
        category_id,
    ):

        exclude = request.query_params.get(
            "exclude"
        )

        products = ProductService.get_related_products(
            category_id,
            exclude_product_id=(
                int(exclude)
                if exclude
                else None
            ),
        )

        serializer = ProductSerializer(
            products,
            many=True,
        )

        return Response(
            serializer.data
        )