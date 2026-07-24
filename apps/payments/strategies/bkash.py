import requests

from django.conf import settings

from .base import PaymentStrategy


class BkashStrategy(PaymentStrategy):
    """
    bKash Tokenized Checkout Strategy.
    """

    def _get_token(self):

        url = (
            f"{settings.BKASH_BASE_URL}"
            "/tokenized/checkout/token/grant"
        )
        
        headers = {
            "username": settings.BKASH_USERNAME,
            "password": settings.BKASH_PASSWORD,
            "Content-Type": "application/json",
        }

        payload = {
            "app_key": settings.BKASH_APP_KEY,
            "app_secret": settings.BKASH_APP_SECRET,
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        print("=" * 80)
        print("STATUS:", response.status_code)
        print("HEADERS:", response.headers)
        print("TEXT:")
        print(response.text)
        print("=" * 80)

        response.raise_for_status()

        return response.json()["id_token"]

    def initiate_payment(self, order):

        token = self._get_token()

        url = (
            f"{settings.BKASH_BASE_URL}"
            "/tokenized/checkout/create"
        )

        headers = {
            "Authorization": token,
            "X-APP-Key": settings.BKASH_APP_KEY,
            "Content-Type": "application/json",
        }

        payload = {
            "mode": "0011",
            "payerReference": str(order.id),
            "callbackURL": settings.BKASH_CALLBACK_URL,
            "amount": str(order.total_amount),
            "currency": "BDT",
            "intent": "sale",
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        return {
            # bKash paymentID becomes transaction_id
            "transaction_id": data["paymentID"],

            # frontend redirects user here
            "client_secret": data["bkashURL"],

            "status": data.get(
                "transactionStatus",
                "PENDING",
            ),

            "raw_response": data,
        }

    def verify_payment(
        self,
        transaction_id,
    ):

        token = self._get_token()

        execute_url = (
            f"{settings.BKASH_BASE_URL}"
            "/tokenized/checkout/execute"
        )

        execute_headers = {
            "Authorization": token,
            "X-APP-Key": settings.BKASH_APP_KEY,
            "Content-Type": "application/json",
        }

        execute_payload = {
            "paymentID": transaction_id,
        }

        execute_response = requests.post(
            execute_url,
            json=execute_payload,
            headers=execute_headers,
            timeout=30,
        )

        execute_response.raise_for_status()

        execute_data = execute_response.json()

        # Query payment status
        query_url = (
            f"{settings.BKASH_BASE_URL}"
            "/tokenized/checkout/payment/status"
        )

        query_response = requests.post(
            query_url,
            json={
                "paymentID": transaction_id,
            },
            headers=execute_headers,
            timeout=30,
        )

        query_response.raise_for_status()

        query_data = query_response.json()

        if query_data.get("transactionStatus") == "Completed":
            status = "SUCCESS"
        else:
            status = "FAILED"

        return {
            "transaction_id": transaction_id,
            "status": status,
            "raw_response": {
                "execute": execute_data,
                "query": query_data,
            },
        }