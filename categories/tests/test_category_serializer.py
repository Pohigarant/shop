import pytest

from categories.models import Category
from categories.serializers import CategorySerializer


@pytest.fixture
def category(db):
    return Category.objects.create(name="test")


@pytest.mark.django_db
def test_category_serializer(category):
    """Тестирование существующего обьекта"""
    serializer = CategorySerializer(instance=category)
    data = serializer.data
    assert data["name"] == category.name
    assert set(data.keys()) == {"id", "name","slug"}

@pytest.mark.django_db
def test_category_deserializer_valid():
    data = {"name": "test1"}
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["name"] == "test1"


@pytest.mark.django_db
def test_category_deserializer_invalid():
    data = {"slug": "test"}
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid() is False
    assert "name" in serializer.errors

@pytest.mark.django_db
def test_category_deserializer_create():
    data = {"name": "test"}
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid()
    cat = serializer.save()
    assert cat.name == "test"
    assert cat.slug == "test"

@pytest.mark.django_db
def test_category_deserializer_update(category):
    data = {"name": "test1"}
    serializer = CategorySerializer(instance=category,data=data,partial=True)
    assert serializer.is_valid() is True
    updated = serializer.save()
    assert updated.name == "test1"
    assert updated.slug == "test"