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


@pytest.mark.django_db
def test_product_serializer_validate_price_positiv(category):
    data = {"name": "test", "price": 500}

    serializer = ProductDetailSerializer(data=data)
    assert serializer.is_valid() is True


@pytest.mark.django_db
def test_product_serializer_validate_price_negativ():
    data = {"name": "test", "price": -500}

    serializer = ProductDetailSerializer(data=data)
    assert serializer.is_valid() is False
    assert "price" in serializer.errors
    assert "не может быть отрицательной" in str(serializer.errors["price"])


@pytest.mark.django_db
def test_product_serializer_create_product():
    data = {"name": "test", "price": 500, "quantity": 5}
    serializer = ProductDetailSerializer(data=data)
    assert serializer.is_valid() is True
    product = serializer.save()
    assert product.name == "test"
    assert product.price == 500
    assert product.quantity == 5
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_product_serializer_update_product(product):
    data = {"price":197}
    serializer = ProductDetailSerializer(product, data=data,partial=True)
    assert serializer.is_valid() is True
    product = serializer.save()
    assert product.name == "test"
    assert product.price == 197


@pytest.mark.django_db
def test_serializer_empty_name():
    data={"name": "", "price": 500}
    serializer = ProductDetailSerializer(data=data)
    assert serializer.is_valid() is False
    assert "name" in serializer.errors

@pytest.mark.django_db
def test_product_serializer_low_quanty():
    data = {"name": "test", "price": 500, "quantity": -55}
    serializer = ProductDetailSerializer(data=data)
    assert serializer.is_valid() is False
    assert "quantity" in serializer.errors


@pytest.mark.django_db
def test_product_serializer_read_only():
    data = {
        "name": "test",
        "price": 500,
        "quantity": 10,
        "id": 9999,  # read_only
        "created_at": "2020-01-01T00:00:00Z",  # read_only
        "updated_at": "2020-01-01T00:00:00Z",  # read_only
        "reviews_count": 100,  # read_only
        "average_rating": 9.9,  # read_only
    }
    serializer = ProductDetailSerializer(data=data)
    assert serializer.is_valid() is True
    product = serializer.save()
    assert product.name == "test"
    assert product.id != 9999
    assert str(product.created_at) != "2020-01-01T00:00:00Z"
    assert serializer.data.get("reviews_count") != 100
    assert serializer.data.get("average_rating") != 9.9




# @pytest.mark.django_db
# def test_get_reviews_count(product, user):
#     # Создаём два отзыва
#     Review.objects.create(product=product, user=user, rating=5)
#     Review.objects.create(product=product, user=user, rating=4)
#     serializer = ProductDetailSerializer(product)
#     count = serializer.get_reviews_count(product)
#     aver = serializer.get_average_rating(product)
#     assert aver == 4.5
#     assert count == 2
