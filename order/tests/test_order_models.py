import pytest
from django.db import IntegrityError
from django.urls import reverse

from categories.models import Category
from order.models import Order, OrderItem
from products.models import Product




@pytest.fixture
def category(db):
    return Category.objects.create(name="test")

@pytest.fixture
def product(db,category):
    return Product.objects.create(name="test1",price=100,quantity=10, category=category)

@pytest.fixture
def order(user):
    return Order.objects.create(user=user)

@pytest.fixture
def order_item(order,product):
    return OrderItem.objects.create(order=order,product=product,price_at_purchase=product.price)

@pytest.mark.django_db
def test_create_order(user):
    order = Order.objects.create(user=user)
    assert order.user == user
    assert order.status == "pending"
    assert order.total_price == 0

@pytest.mark.django_db
def test_order_str(order):
    assert str(order) == f"Заказ #{order.pk} ({order.status})"


@pytest.mark.django_db
def test_create_order_item(order,order_item,product):
    assert order_item.order == order
    assert order_item.product == product
    assert order_item.quantity == 1
    assert order_item.price_at_purchase == product.price