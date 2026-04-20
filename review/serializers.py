from rest_framework import serializers

import review
from products.models import Product
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())
    class Meta:
        model = Review
        fields = ["id", "user", "rating", "product", "created_at", "text"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        user = self.context['request'].user
        product = data['product']
        if self.instance is None:
            if Review.objects.filter(user=user, product=product).exists():
                raise serializers.ValidationError("Вы уже оставили отзыв на этот товар.")
        return data