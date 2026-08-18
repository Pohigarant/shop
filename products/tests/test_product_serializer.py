import pytest
from django.contrib.auth import get_user_model

from categories.models import Category
from products.models import Product
from products.serializers import ProductDetailSerializer
from review.models import Review


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="12345")


@pytest.fixture
def category(db):
    return Category.objects.create(name="Старое название")


@pytest.fixture
def product(category):
    return Product.objects.create(name="test", category=category, price=500)


def test_product_serializer_validate_price_negativ(category):
    data = {"name": "test", "category": category.id, "price": -500}

    serializer = ProductDetailSerializer(data=data)
    assert serializer.is_valid() is False
    assert "price" in serializer.errors
    assert "не может быть отрицательной" in str(serializer.errors["price"])


def test_product_serializer_validate_price_positiv(category):
    data = {"name": "test", "category": category.id, "price": 500}

    serializer = ProductDetailSerializer(data=data)
    assert serializer.is_valid() is True


def test_product_reviews_count_empty(product):
    serializer = ProductDetailSerializer(instance=product)
    assert serializer.data["reviews_count"] == 0


def test_get_reviews_count(product, user):
    # Создаём два отзыва
    Review.objects.create(product=product, user=user, rating=5)
    Review.objects.create(product=product, user=user, rating=4)
    serializer = ProductDetailSerializer
    count = serializer.get_reviews_count(product)
    aver = serializer.get_average_rating(product)
    assert aver == 4.5
    assert count == 2
