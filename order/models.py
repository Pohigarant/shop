from django.db import models

from products.models import Product
from shop1 import settings

status_choices = [
    ('pending','pending'),
    ('confirmed','confirmed'),
    ('shipped','shipped'),
    ('delivered','delivered'),
    ('cancelled','cancelled'),
]

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order')

    status = models.CharField(choices=status_choices, default='pending', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)



