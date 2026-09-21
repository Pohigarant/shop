from rest_framework import permissions

from order.models import OrderItem, OrderStatus


class IsOwnerOrAdmin(permissions.BasePermission):
    message = "Вы не можете редактировать"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, "user"):
            return obj.user == request.user or request.user.is_staff
            # Если объект сам является пользователем
        return obj == request.user or request.user.is_staff


class IsCartOwnerOrAdmin(permissions.BasePermission):
    """Класс разрешения для корзины"""

    message = "Вы не можете редактировать"

    def has_object_permission(self, request, view, obj):
        return obj.cart.user == request.user or request.user.is_staff


class HasPurchasedProduct(permissions.BasePermission):
    message = "Отзыв можно оставить только на купленный товар"

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        product_pk = view.kwargs.get("prod_pk") or request.data.get("product")
        if not product_pk:
            return False
        return OrderItem.objects.filter(
            order__user=request.user,
            order__status=OrderStatus.DELIVERED,
            product_id=product_pk,  # по id, не по имени
        ).exists()
