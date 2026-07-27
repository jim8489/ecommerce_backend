from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import stripe

from django.conf import settings

from rest_framework.permissions import AllowAny

from .models import Payment
from .serializers import (
    PaymentConfirmSerializer,
    PaymentInitiateSerializer,
    PaymentSerializer,
)
from .services import PaymentService


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Payment API

    GET     /payments/
    GET     /payments/{id}/

    POST    /payments/initiate/
    POST    /payments/confirm/

    POST    /payments/webhook/
    """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = (
            Payment.objects
            .select_related(
                "order",
                "order__user",
            )
            .order_by("-created_at")
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(
            order__user=self.request.user
        )

    def get_object(self):

        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs["pk"],
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="initiate",
    )
    def initiate(self, request):

        serializer = PaymentInitiateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = PaymentService.initiate_payment(
            order_id=serializer.validated_data["order_id"],
            provider=serializer.validated_data["provider"],
        )

        return Response(
        {
             "payment": PaymentSerializer(
                  result["payment"]
            ).data,
            "client_secret": result["client_secret"],
        },
        status=status.HTTP_201_CREATED,
        )
    @action(
        detail=False,
        methods=["post"],
        url_path="confirm",
    )
    def confirm(self, request):

        serializer = PaymentConfirmSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        payment = PaymentService.confirm_payment(
            serializer.validated_data["transaction_id"]
        )

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_200_OK,
        )
    @action(
        detail=False,
        methods=["post"],
        url_path="stripe/webhook",
        permission_classes=[AllowAny],
)
    def webhook(self, request):

        payload = request.body

        signature = request.headers.get(
           "Stripe-Signature"
    )

        try:

            event = stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET,
        )

        except (
            ValueError,
            stripe.error.SignatureVerificationError,
        ):

            return Response(
                {"detail": "Invalid webhook."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if event["type"] == "payment_intent.succeeded":

            intent = event["data"]["object"]

            PaymentService.process_webhook(
            intent["id"]
        )

        return Response(
            {"received": True},
            status=status.HTTP_200_OK,
        )
        
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class BkashCallbackView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):

        payment_id = request.GET.get("paymentID")
        status = request.GET.get("status", "").lower()

        if status == "success":

            PaymentService.confirm_payment(payment_id)

            return HttpResponseRedirect(
                "/payment/success/"
            )

        elif status == "failure":

            payment = Payment.objects.filter(
                transaction_id=payment_id
            ).first()

            if payment:
                payment.status = Payment.Status.FAILED
                payment.save(update_fields=["status"])

            return HttpResponseRedirect(
                "/payment/failed/"
            )

        elif status == "cancel":

            payment = Payment.objects.filter(
                transaction_id=payment_id
            ).first()

            if payment:
                payment.status = Payment.Status.FAILED
                payment.save(update_fields=["status"])

            return HttpResponseRedirect(
                "/payment/cancelled/"
            )

        return Response(
            {"detail": "Invalid callback"},
            status=400,
        )