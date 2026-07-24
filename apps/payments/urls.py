from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet
from .callbacks import BkashCallbackView

from .webhooks import StripeWebhookView

router = DefaultRouter()

router.register(
    "",
    PaymentViewSet,
    basename="payments",
)

urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
    path(
        "stripe/webhook/",
        StripeWebhookView.as_view(),
        name="stripe-webhook",
    ),
    
    path(
        "bkash/callback/",
        BkashCallbackView.as_view(),
        name="bkash-callback",
    ),
]