from rest_framework import serializers

from order.models import OrderItem, Order
from products.models import Product
from users.models import User


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    price_at_purchase = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Order
        fields = ['id','status', 'user', 'items', 'total_price', 'created_at']