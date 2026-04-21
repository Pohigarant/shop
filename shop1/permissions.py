from rest_framework import permissions

from cart.models import Cart, CartItem
from products.models import Product


class IsOwnerOrAdmin(permissions.BasePermission):
    message = 'Вы не можете редактировать'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_staff
            # Если объект сам является пользователем
        return obj == request.user or request.user.is_staff


class IsCartOwnerOrAdmin(permissions.BasePermission):
    """Класс разрешения для корзины"""
    message = 'Вы не можете редактировать'

    def has_object_permission(self, request, view, obj):

        return obj.cart.user == request.user or request.user.is_staff


class HasPurchasedProduct(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not  user.is_authenticated:
            return False

        product_name = request.data.get("product")
        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            return False

        return CartItem.objects.filter(cart__user=user,product=product).exists()



