import pytest

from categories.models import Category
from products.models import Product
from review.models import Review


@pytest.fixture
def category(db):
    return Category.objects.create(name="test")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="test1", price=100, quantity=10, category=category
    )


@pytest.fixture
def review(user, product):
    return Review.objects.create(
        user=user, product=product, rating=5, text="Отлично"
    )


@pytest.mark.django_db
def test_create_review(review, user, product):
    assert review.user == user
    assert review.product == product
    assert review.rating == 5
    assert review.text == "Отлично"
