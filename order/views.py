from django.shortcuts import render
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart
from order.models import Order, OrderItem
from order.serializers import OrderSerializer
from shop1.permissions import IsOwnerOrAdmin


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        cart,_ = Cart.objects.get_or_create(user=user)
        if not cart.items.exists():
           raise serializers.ValidationError("Корзина пуста")
        order = Order.objects.create(user=user, total_price = 0)

        total = 0
        for item in cart.items.all():

            order_item = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity,
                                                  price_at_purchase=item.product.price)
            total+= order_item.quantity*order_item.product.price

        order.total_price = total
        order.save()

        cart.items.all().delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if  order.status != 'pending':
            return Response({"detail": "Статус не "}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'cancelled'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
