
from django.urls import path, include
from rest_framework import routers

from cart import views
from cart.views import CartItemViewSet, CartView

router = routers.DefaultRouter()
router.register(r'cartitem', CartItemViewSet)



cart_detail = CartView.as_view({'get': 'retrieve'})


urlpatterns = [
    path('', include(router.urls)),
    path('cart/', cart_detail, name="cart"),

]