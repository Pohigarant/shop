from django.db import models
from rest_framework import status
from rest_framework.response import Response

from products.models import Product
from users.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True, blank=True, related_name="сart",
                                verbose_name="Покупатель")


    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             related_name="items",
                             verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="cart_items"
                                ,verbose_name="Товары")

    quantity = models.PositiveIntegerField(default=1,verbose_name="Количество")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        unique_together = (('cart', 'product'),)

