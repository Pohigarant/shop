from django.urls import include, path
from rest_framework import routers

from cart.views import CartItemViewSet, CartView

router = routers.DefaultRouter()
router.register(r"cartitem", CartItemViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "cart/my/", CartView.as_view({"get": "my"}), name="cart-my"
    ),  # добавить
    path("cart/", CartView.as_view({"get": "retrieve"}), name="cart"),
]
