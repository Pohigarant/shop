from django.urls import include, path
from rest_framework import routers

from cart.views import CartItemViewSet, CartView

router = routers.DefaultRouter()

router.register(r"cartitem", CartItemViewSet)
router.register(r"cart", CartView, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]
