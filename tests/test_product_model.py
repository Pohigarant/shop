import pytest
from django.db import IntegrityError
from django.urls import reverse

from categories.models import Category
from products.models import Product


@pytest.fixture
def category():
    return Category.objects.create(name="test")

@pytest.fixture
def product(category):
    return Product.objects.create(name="test",category=category, price=500)

@pytest.mark.django_db
def test_product_creation():
    product = Product.objects.create(name="Phone", price=500)
    assert product.name == "Phone"
    assert product.price == 500
    assert product.quantity == 0
    assert product.is_active is True
    assert product.pk is not None
    assert Product.objects.count() == 1

@pytest.mark.django_db
def test_product_category_nullable_and_blank():

    product = Product.objects.create(name="Orphan", price=100)
    assert product.category is None

@pytest.mark.django_db
def test_product_with_category(category):
    product = Product.objects.create(name="Tablet", price=300, category=category)
    assert product.category == category
    assert product.category.name == "test"

@pytest.mark.django_db
def test_on_delete_set_null(category, product):
    category.delete()
    assert not Category.objects.filter(pk=category.pk).exists()  # категория удалена
    product.refresh_from_db()
    assert product.category is None
    assert Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_slug_unique():
    Product.objects.create(name="Chair", price=100)
    with pytest.raises(IntegrityError):
        Product.objects.create(name="Chair", price=150)

@pytest.mark.django_db
def test_product_str(product):
    assert str(product) == product.name

@pytest.mark.django_db
def test_default_quantity():
    product = Product.objects.create(name="TV", price=500)
    assert product.quantity == 0

@pytest.mark.django_db
def test_default_is_active():
    product = Product.objects.create(name="Radio", price=30)
    assert product.is_active is True
