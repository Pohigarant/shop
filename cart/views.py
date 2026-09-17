from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from shop1.permissions import IsCartOwnerOrAdmin


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsCartOwnerOrAdmin,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(
                cart__user=self.request.user
            ).select_related("product")
        return CartItem.objects.none()

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        cart_item = cart.add_product(product, quantity)
        response_serializer = self.get_serializer(cart_item)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    def perform_update(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
        return serializer


class CartView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        cart = Cart.objects.prefetch_related("items__product").get(pk=cart.pk)
        return cart

    @action(detail=False, methods=["get"])
    def my(self, request):
        cart = self.get_object()
        serializer = CartSerializer(cart, many=False)
        return Response(serializer.data)
