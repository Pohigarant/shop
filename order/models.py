from django.conf import settings
from django.db import models

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
        related_name="order",
    )

    status = models.CharField(
        choices=status_choices, default="pending", max_length=50
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    def __str__(self):
        return f"Заказ #{self.pk} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
