from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings

from cart.models import Cart, CartItem
from products.models import Product


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(pre_delete,sender = Product)
def delete_products_from_carts(sender, instance, **kwargs):
    CartItem.objects.filter(product=instance).delete()