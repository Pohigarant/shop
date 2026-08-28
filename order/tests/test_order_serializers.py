import pytest
from categories.models import Category
from order.models import Order, OrderItem
from order.serializers import OrderItemSerializer, OrderSerializer
from products.models import Product


@pytest.fixture
def category(db):
    return Category.objects.create(name="test")


@pytest.fixture
def product(db, category):
    return Product.objects.create(name="test1", price=100, quantity=10, category=category)

@pytest.fixture
def order(user):
    return Order.objects.create(user=user)

@pytest.fixture
def order_item(order, product):
    return OrderItem.objects.create(order=order, product=product,price_at_purchase=product.price)

@pytest.mark.django_db
def test_order_serializer_with_items(order, order_item):
    serializer = OrderSerializer(order)
    data = serializer.data
    assert data["id"] == order.id
    assert data["status"] == "pending"
    assert len(data["items"]) == 1
    assert data["total_price"] == "0.00"
    assert data["items"][0]["quantity"] == order_item.quantity
    assert data["items"][0]["price_at_purchase"] == f"{order_item.price_at_purchase:.2f}"

@pytest.mark.django_db
def test_order_item_serializer(order_item,product):
    serializer = OrderItemSerializer(order_item)
    data = serializer.data
    assert data["id"] == order_item.id
    assert data["product"] == product.id
    assert data["quantity"] == order_item.quantity
    assert data["price_at_purchase"] == f"{order_item.price_at_purchase:.2f}"
    assert "order" not in data


