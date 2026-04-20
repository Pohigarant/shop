from django.db.models import Avg
from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    # category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "model", "price", "quantity", "category", 'reviews_count']
        read_only_fields = ["id", "created_at", "updated_at"]


    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value


    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(Avg("rating"))["rating__avg"]



class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "category"]


class ProductDetailSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ["slug", "article", "product_info", "is_active", "created_at",
                                                  "updated_at","average_rating"]
