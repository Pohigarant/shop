from rest_framework import serializers

from products.models import Product
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())
    class Meta:
        model = Review
        fields = ["id", "user", "rating", "product", "created_at", "text"]
        read_only_fields = ["id", "created_at"]