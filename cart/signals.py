from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from cart.models import Cart, CartItem


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def set_cart_updated_at(sender, instance, **kwargs):
    if instance.cart:
        instance.cart.save()
