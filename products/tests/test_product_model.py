import pytest
from django.db import IntegrityError
from django.urls import reverse

from categories.models import Category
from products.models import Product


@pytest.fixture
def category(db):
    return Category.objects.create(name="test")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="test1", price=100, quantity=10, category=category
    )


@pytest.mark.django_db
def test_product_slug(product):
    assert product.slug == "test1"


@pytest.mark.django_db
def test_product_rename_slug(product):
    old_slug = product.slug
    product.name = "test2"
    product.save()
    product.refresh_from_db()
    assert product.slug != old_slug
    assert product.slug == "test2"


@pytest.mark.django_db
def test_product_slug_match(product, category):

    with pytest.raises(IntegrityError):
        Product.objects.create(
            name="test1", price=100, quantity=10, category=category
        )


@pytest.mark.django_db
def test_product_str(product):
    assert str(product) == "test1"


@pytest.mark.django_db
def test_product_get_absolut_url(product):
    expected_url = reverse("product-detail", kwargs={"slug": product.slug})
    assert product.get_absolute_url() == expected_url


@pytest.mark.django_db
def test_product_delete_category(product, category):
    product.category.delete()
    product.refresh_from_db()
    assert Product.objects.filter(pk=product.pk).exists()
    assert product.category is None
