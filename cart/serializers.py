from rest_framework import serializers
from cart.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    item_total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'product_name', 'quantity', 'product_price', 'item_total_price')

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_price(self, obj):
        return obj.product.price

    def get_item_total_price(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id','items', 'total_cart','created_at', 'updated_at')

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())