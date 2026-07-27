from django.core.cache import cache

from apps.products.models import Category, Product
import logging

logger = logging.getLogger(__name__)

class RecommendationService:

    CACHE_KEY = "category_tree"

    @classmethod
    def get_tree(cls):

        tree = cache.get(cls.CACHE_KEY)

        if tree is not None:
            return tree

        tree = {}

        for category in (
            Category.objects
            .select_related("parent")
        ):

            parent = category.parent_id

            tree.setdefault(parent, []).append(category.id)

        cache.set(
            cls.CACHE_KEY,
            tree,
            timeout=60 * 60,
        )

        return tree

    @classmethod
    def dfs(cls, tree, node, visited):

        if node in visited:
            return

        visited.append(node)

        for child in tree.get(node, []):

            cls.dfs(
                tree,
                child,
                visited,
            )

    @classmethod
    def recommended_products(
        cls,
        category_id,
    ):

        tree = cls.get_tree()

        categories = []

        cls.dfs(
            tree,
            category_id,
            categories,
        )

        return (
            Product.objects
            .filter(
                category_id__in=categories,
                status=Product.Status.ACTIVE,
            )
        )