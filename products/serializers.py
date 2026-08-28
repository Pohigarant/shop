from rest_framework import serializers

from categories.serializers import CategorySerializer
from products.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    # category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "model",
            "price",
            "quantity",
            "category",
            "reviews_count",
            "average_rating",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Цена не может быть отрицательной"
            )
        return value


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "price", "category")
