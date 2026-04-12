from rest_framework import serializers

from categories.models import Category
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name',queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = ["id", "name","model", "price", "quantity", "category"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value