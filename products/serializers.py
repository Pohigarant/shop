from django.db.models import Avg
from rest_framework import serializers

from categories.serializers import CategorySerializer
from products.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    # category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

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

    # @staticmethod
    # def get_reviews_count(obj):
    #     return obj.reviews.count()
    #
    # @staticmethod
    # def get_average_rating(obj):
    #     return obj.reviews.aggregate(Avg("rating"))["rating__avg"]

    @staticmethod
    def get_reviews_count(obj):
        return getattr(obj, 'reviews_count', obj.reviews.count())

    @staticmethod
    def get_average_rating(obj):
        avg = getattr(obj, 'average_rating', None)
        if avg is None:
            avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return avg


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "price", "category")
