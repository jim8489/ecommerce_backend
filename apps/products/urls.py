from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ProductViewSet,
    RelatedProductsView,
)

router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet,
)

router.register(
    "products",
    ProductViewSet,
)

urlpatterns = [
    path(
        "",
        include(router.urls),
    ),

    path(
        "products/recommendations/<int:category_id>/",
        RelatedProductsView.as_view(),
        name="product-recommendations",
    ),
]