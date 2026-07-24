from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order
from .serializers import (
    CreateOrderSerializer,
    OrderSerializer,
)
from .services import OrderService


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = (
            Order.objects
            .select_related("user")
            .prefetch_related(
                "items",
                "items__product",
            )
            .order_by("-created_at")
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(
            user=self.request.user
        )

    def get_serializer_class(self):

        if self.action == "create":
            return CreateOrderSerializer

        return OrderSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True,
        )

        order = OrderService.create_order(
            user=request.user,
            items=serializer.validated_data["items"],
        )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )