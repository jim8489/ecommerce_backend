from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.products.models import Category


CACHE_KEY = "category_tree"


@receiver(post_save, sender=Category)
def clear_cache_on_save(sender, **kwargs):

    cache.delete(CACHE_KEY)


@receiver(post_delete, sender=Category)
def clear_cache_on_delete(sender, **kwargs):

    cache.delete(CACHE_KEY)