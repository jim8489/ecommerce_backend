from django.core.cache import cache
def setUp(self):

    cache.clear()

CATEGORY_TREE_KEY = "category_tree"


def get_cached_tree():
    """
    Return cached category tree.
    """

    return cache.get(CATEGORY_TREE_KEY)


def set_cached_tree(tree):
    """
    Cache category tree for 1 hour.
    """

    cache.set(
        CATEGORY_TREE_KEY,
        tree,
        timeout=60 * 60,
    )


def invalidate_category_cache():
    """
    Remove cached category tree.
    """

    cache.delete(CATEGORY_TREE_KEY)