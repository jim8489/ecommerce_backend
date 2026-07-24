from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.products.models import Product

from .models import Order, OrderItem


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(user, items):

        order = Order.objects.create(
            user=user,
        )

        total_amount = Decimal("0.00")

        order_items = []

        for item in items:

            product = get_object_or_404(
                Product,
                pk=item["product_id"],
                status=Product.Status.ACTIVE,
            )

            quantity = item["quantity"]

            price = product.price

            subtotal = price * quantity

            total_amount += subtotal

            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price,
                    subtotal=subtotal,
                )
            )

        OrderItem.objects.bulk_create(order_items)

        order.total_amount = total_amount

        order.save(update_fields=["total_amount"])

        return order