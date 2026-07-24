import logging

from django.shortcuts import redirect

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .services import PaymentService

logger = logging.getLogger(__name__)


class BkashCallbackView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):

        logger.info(request.GET)

        payment_id = request.GET.get(
            "paymentID"
        )

        status = request.GET.get(
            "status"
        )

        if not payment_id:

            return redirect(
                "http://localhost:5173/payment-failed"
            )

        try:

            PaymentService.process_webhook(
                payment_id
            )

            return redirect(
                "http://localhost:5173/payment-success"
            )

        except Exception as e:

            logger.exception(e)

            return redirect(
                "http://localhost:5173/payment-failed"
            )