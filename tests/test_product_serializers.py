import pytest

from categories.models import Category
from products.models import Product
from products.serializers import ProductSerializer


@pytest.fixture
def category(db):
    return Category.objects.create(name="Electronics")


# Фикстура продукта (с категорией)
@pytest.fixture
def product(category):
    return Product.objects.create(
        name="Laptop",
        price=999.99,
        category=category
    )


@pytest.mark.django_db
def test_product_creat(product):
    serializer = ProductSerializer(instance=product)
    data = serializer.data
    assert data["name"] == product.name
    assert data["category"]["name"] == product.category.name


@pytest.mark.django_db
def test_product_create(category):
    product = Product.objects.create(
        name="Smartphone",
        price=599.99,
        category=category
    )
    assert product.name == "Smartphone"
    assert product.price == 599.99
    assert product.category.name == "Electronics"





@pytest.mark.django_db
def test_create_product_without_fixture():
    """Создание продукта с категорией, созданной прямо в тесте"""
    category = Category.objects.create(name="Books")
    product = Product.objects.create(
        name="Django Book",
        price=49.99,
        category=category
    )
    assert product.name == "Django Book"
    assert product.price == 49.99
    assert product.category.name == "Books"
    assert Product.objects.count() == 1



