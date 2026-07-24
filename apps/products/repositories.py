from django.shortcuts import get_object_or_404

from .models import Product


class ProductRepository:

    @staticmethod
    def all():
        return (
            Product.objects
            .select_related("category")
            .all()
        )

    @staticmethod
    def get(pk):
        return get_object_or_404(
            Product.objects.select_related("category"),
            pk=pk,
        )

    @staticmethod
    def create(**kwargs):
        return Product.objects.create(**kwargs)

    @staticmethod
    def update(product):
        product.save()
        return product

    @staticmethod
    def delete(product):
        product.delete()

    @staticmethod
    def get_related(category_ids):
        return (
            Product.objects
            .select_related("category")
            .filter(
                category_id__in=category_ids,
                status=Product.Status.ACTIVE,
            )
            .order_by("-created_at")
        )