from django.core.cache import cache
from django.db import models, transaction
from django.db.models import Avg, Count, Value
from django.db.models.functions import Coalesce
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from products.models import Product
from review.models import Review


def update_product_rating(product_id):
    stats = Review.objects.filter(product_id=product_id).aggregate(
        average=Coalesce(
            Avg("rating"), Value(0), output_field=models.DecimalField()
        ),
        count=Count("id"),
    )

    Product.objects.filter(pk=product_id).update(
        average_rating=stats["average"],
        reviews_count=stats["count"],
    )
    cache.delete("products:popular:v1")


@receiver(post_save, sender=Review, dispatch_uid="rating_on_save")
@receiver(post_delete, sender=Review, dispatch_uid="rating_on_delete")
def refresh_product_rating(sender, instance, **kwargs):
    product_id = instance.product_id
    transaction.on_commit(lambda: update_product_rating(product_id))
