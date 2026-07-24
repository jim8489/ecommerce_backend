from .models import Payment
from .strategies.bkash import BkashStrategy
from .strategies.stripe import StripeStrategy


class PaymentFactory:

    @staticmethod
    def get(provider):

        strategies = {
            Payment.Provider.STRIPE: StripeStrategy(),
            Payment.Provider.BKASH: BkashStrategy(),
        }

        try:
            return strategies[provider]

        except KeyError:
            raise ValueError(
                f"Unsupported payment provider: {provider}"
            )