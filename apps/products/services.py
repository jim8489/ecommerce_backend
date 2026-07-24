from .cache import (
    get_cached_tree,
    set_cached_tree,
)
from .dfs import CategoryDFS
from .models import Category
from .repositories import ProductRepository


class ProductService:
    """
    Business logic for Product Management
    and Product Recommendation.
    """

    @staticmethod
    def create_product(validated_data):
        return ProductRepository.create(
            **validated_data
        )

    @staticmethod
    def update_product(
        product,
        validated_data,
    ):

        for field, value in validated_data.items():
            setattr(
                product,
                field,
                value,
            )

        return ProductRepository.update(
            product
        )

    @staticmethod
    def delete_product(product):

        ProductRepository.delete(product)

    @staticmethod
    def get_category_tree():
        """
        Build the category tree once
        and cache it.
        """

        tree = get_cached_tree()

        if tree is None:

            categories = (
                Category.objects
                .all()
            )

            tree = CategoryDFS.build_tree(
                categories
            )

            set_cached_tree(tree)

        return tree

    @staticmethod
    def get_related_products(
        category_id,
        exclude_product_id=None,
    ):
        """
        Return products from the selected
        category and all descendant
        categories using DFS traversal.
        """

        tree = (
            ProductService.get_category_tree()
        )

        descendant_ids = (
            CategoryDFS.traverse(
                tree,
                category_id,
            )
        )

        category_ids = [
            category_id,
            *descendant_ids,
        ]

        queryset = (
            ProductRepository.get_related(
                category_ids
            )
        )

        if exclude_product_id is not None:

            queryset = queryset.exclude(
                id=exclude_product_id
            )

        return queryset