from django.conf import settings
from django.db import models
from django.db.models import Q

from products.models import Product

status_choices = [
    ("pending", "pending"),
    ("confirmed", "confirmed"),
    ("shipped", "shipped"),
    ("delivered", "delivered"),
    ("cancelled", "cancelled"),
]


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    status = models.CharField(
        choices=status_choices, default="pending", max_length=50
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Итоговая стоимость",
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("-created_at",)
        indexes = (models.Index(fields=["user", "-created_at"]),)

    def __str__(self):
        return f"Заказ #{self.pk} ({self.status})"

    def recalculate_total(self):
        self.total_price = sum(
            i.price_at_purchase * i.quantity for i in self.items.all()
        )
        self.save(update_fields=["total_price"])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"
        constraints = (
            models.CheckConstraint(
                condition=Q(quantity__gte=1),
                name="order_item_quantity_at_least_one",
            ),
            models.CheckConstraint(
                condition=Q(price_at_purchase__gte=0),
                name="order_item_price_non_negative",
            ),
        )

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
