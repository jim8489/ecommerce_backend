from abc import ABC, abstractmethod


class PaymentStrategy(ABC):

    @abstractmethod
    def initiate_payment(
        self,
        order,
    ):
        pass

    @abstractmethod
    def verify_payment(
        self,
        transaction_id,
    ):
        pass