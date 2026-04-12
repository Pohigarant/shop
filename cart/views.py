from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from cart.models import CartItem, Cart
from cart.serializers import CartItemSerializer, CartSerializer
from shop1.permissions import IsCartOwnerOrAdmin


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsCartOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(cart__user=self.request.user)
        return CartItem.objects.none()


class CartView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart
