from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q

from products.models import Product
from users.models import User


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Покупатель",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def add_product(self, product, quantity=1):
        if quantity > product.quantity:
            raise ValidationError(
                f"Недостаточно товара '{product.name}' на складе. Доступно: {product.quantity} шт."
            )
        item, created = self.items.get_or_create(
            product=product, defaults={"quantity": quantity}
        )
        if not created:
            if item.quantity + quantity > product.quantity:
                raise ValidationError(
                    f"Невозможно добавить {quantity} шт. В корзине уже {item.quantity} шт., а на складе всего {product.quantity} шт."
                )

            item.quantity = F("quantity") + quantity
            item.save(update_fields=["quantity"])
            item.refresh_from_db()  # Сбрасываем F() выражение в обычное число в памяти Python
        return item

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    @property
    def total_price(self):
        return sum(i.line_total for i in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Корзина",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="Товары",
    )

    quantity = models.PositiveIntegerField(
        default=1, verbose_name="Количество"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        unique_together = (("cart", "product"),)
        constraints = (
            models.CheckConstraint(
                condition=Q(quantity__gte=1), name="cart_quantity_not_negative"
            ),
        )

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    @property
    def line_total(self):
        return self.product.price * self.quantity

    def clean(self):
        super().clean()
        if self.product and self.quantity > self.product.quantity:
            raise ValidationError(
                {
                    "quantity": f"Запрашиваемое количество ({self.quantity} шт.) превышает остаток на складе ({self.product.quantity} шт.)."
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Принудительно запускает метод clean() перед сохранением в БД
        super().save(*args, **kwargs)
