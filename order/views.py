from django.db import transaction
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart, CartItem
from order.models import Order, OrderItem
from order.serializers import OrderSerializer
from products.models import Product
from shop1.permissions import IsOwnerOrAdmin


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()

    # @transaction.atomic
    # def create(self, request, *args, **kwargs):
    #     cart = get_object_or_404(Cart, user=request.user)
    #     items = list(cart.items.select_related("product").select_for_update())
    #     if not items:
    #         raise serializers.ValidationError("Корзина пуста")
    #     for item in items:
    #         if item.product.quantity < item.quantity:
    #             raise serializers.ValidationError(
    #
    #                 f"Недостаточно товара «{item.product.name}»")
    #
    #
    #     order = Order.objects.create(user=request.user, total_price=0)
    #
    #     total = 0
    #     for item in cart.items.all():
    #         order_item = OrderItem.objects.create(
    #             order=order,
    #             product=item.product,
    #             quantity=item.quantity,
    #             price_at_purchase=item.product.price,
    #         )
    #         total += order_item.quantity * order_item.product.price
    #
    #     order.total_price = total
    #     order.save()
    #
    #     cart.items.all().delete()
    #     serializer = self.get_serializer(order)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        items = list(cart.items.select_related("product"))
        if not items:
            raise serializers.ValidationError("Корзина пуста")
        product_ids = [item.product_id for item in items]
        products = Product.objects.select_for_update().filter(id__in=product_ids)
        product_map = {p.id: p for p in products}
        for item in items:
            product = product_map[item.product_id]
            if product.quantity < item.quantity:
                raise serializers.ValidationError(
                    f"Недостаточно товара «{product.name}»"
                )
            Product.objects.filter(pk=product.pk).update(
                quantity=F("quantity") - item.quantity
            )
            order = Order.objects.create(user=request.user, total_price=0)
            total = 0
            for item in items:
               order_item = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.price,
                )
            total += order_item.quantity * order_item.price_at_purchase

            order.total_price = total
            order.save(update_fields=["total_price"])


            CartItem.objects.filter(pk__in=[item.pk for item in items]).delete()


            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status != "pending":
            return Response(
                {"detail": "Статус не "}, status=status.HTTP_400_BAD_REQUEST
            )
        order.status = "cancelled"
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
