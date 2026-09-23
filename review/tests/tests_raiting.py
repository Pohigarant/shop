from decimal import Decimal

import pytest

from categories.models import Category
from products.models import Product
from review.models import Review

pytestmark = pytest.mark.redis


@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")


@pytest.fixture
def product(category):
    return Product.objects.create(
        name="Test Product", category=category, price=5.00
    )


def test_rating(db, django_capture_on_commit_callbacks, product, user):
    with django_capture_on_commit_callbacks(execute=True):
        Review.objects.create(product=product, user=user, rating=5, text="ok")
    product.refresh_from_db()
    assert product.average_rating == Decimal("5.00")
