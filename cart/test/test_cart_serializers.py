import pytest
from django.db import IntegrityError
from django.urls import reverse

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from categories.models import Category
from products.models import Product


@pytest.fixture
def cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@pytest.fixture
def category(db):
    return Category.objects.create(name="test")


@pytest.fixture
def product(db, category):
    return Product.objects.create(name="test1", price=100, quantity=10, category=category)


@pytest.fixture
def cartitem(cart, product):
    return CartItem.objects.create(cart=cart, product=product)


@pytest.mark.django_db
def test_cart_serializer_with_items(cart, cartitem,product):
    serializer = CartSerializer(cart)
    data = serializer.data

    assert isinstance(data["items"], list)
    assert len(data["items"]) == 1

    item = data["items"][0]
    assert item["product_name"] == product.name
    assert item["item_total_price"] == product.price * cartitem.quantity

    assert data["total_price"] == product.price * cartitem.quantity


@pytest.mark.django_db
def test_cart_item_serializer_create(cart, product):
    data = {

        "product": product.id,
        "quantity": 2,
    }
    serializer = CartItemSerializer(data=data)
    assert serializer.is_valid() is True
    saved_item = serializer.save(cart=cart)
    assert saved_item.cart == cart  # сравниваем объект Cart
    assert saved_item.product == product  # сравниваем объект Product
    assert saved_item.quantity == 2
    assert CartItem.objects.count() == 1


@pytest.mark.django_db
def test_cart_total_price_multiple_items(cart):
    product1=Product.objects.create(name="test1", price=100, quantity=1)
    product2=Product.objects.create(name="test2", price=200, quantity=2)
    CartItem.objects.create(cart=cart, product=product1, quantity=1)
    CartItem.objects.create(cart=cart, product=product2, quantity=2)
    serializer = CartSerializer(cart)
    data = serializer.data
    assert len(data["items"]) == 2
    assert data["total_price"] == 500

@pytest.mark.django_db
def test_cart_item_serializer_missing_product(cart,product):
    data = {

        "quantity": 2,
    }
    serializer = CartItemSerializer(data=data)
    assert serializer.is_valid() is False
    assert "product" in serializer.errors