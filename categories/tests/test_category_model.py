import pytest
from django.db import IntegrityError
from django.urls import reverse

from categories.models import Category


@pytest.fixture
def category(db):
    return Category.objects.create(name="test")


@pytest.mark.django_db
def test_category_creat():
    cat = Category.objects.create(name="test1")
    assert cat.name == "test1"
    assert Category.objects.count() == 1
    assert cat.pk is not None
    assert cat.slug == "test1"


@pytest.mark.django_db
def test_category_slug_unique(category):
    Category.objects.create(name="test1")
    with pytest.raises(IntegrityError):
        Category.objects.create(name="test1")


@pytest.mark.django_db
def test_category_str_repr(category):
    assert str(category) == "test"


@pytest.mark.django_db
def test_category_get_absolute_url(category):
    expected_url = reverse("categories-detail", kwargs={"pk": category.pk})
    assert category.get_absolute_url() == expected_url

@pytest.mark.django_db
def test_category_get_slug():
    cat=Category.objects.create(name="test")
    old_slug = cat.slug
    cat.name = "test1"
    cat.save()
    cat.refresh_from_db()
    assert cat.slug != old_slug
    assert cat.slug == "test1"
