from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver

from cart.models import Cart, CartItem
from products.models import Product


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(pre_delete, sender=Product)
def delete_products_from_carts(sender, instance, **kwargs):
    CartItem.objects.filter(product=instance).delete()


@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def set_cart_updated_at(sender, instance, **kwargs):
    if instance.cart:
        instance.cart.save()
