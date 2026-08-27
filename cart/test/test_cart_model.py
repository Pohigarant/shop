import pytest
from django.db import IntegrityError
from django.urls import reverse

from cart.models import Cart, CartItem
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
def test_one_cart_one_user(cart,user):
    with pytest.raises(IntegrityError):
        Cart.objects.create(user=user)


@pytest.mark.django_db
def test_cart_str(cart, user):
    assert str(cart) == f"Корзина пользователя {user.username}"


@pytest.mark.django_db
def test_cart_item(cart,product):
    cart_item=CartItem.objects.create(cart=cart,product=product)
    assert cart_item.cart == cart
    assert cart_item.product == product
    assert cart_item.quantity == 1

def test_cartitem_one_product(cartitem,cart,product):
    with pytest.raises(IntegrityError):
        CartItem.objects.create(cart=cart,product=product)

