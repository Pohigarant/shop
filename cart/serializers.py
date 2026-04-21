from rest_framework import serializers
from cart.models import CartItem, Cart
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)
    product_price = serializers.SerializerMethodField(read_only=True)
    item_total_price = serializers.SerializerMethodField(read_only=True)
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), write_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product_name', 'quantity', 'product_price', 'item_total_price','cart', 'product')

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
        fields = ('id','items', 'total_price','created_at', 'updated_at')

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())