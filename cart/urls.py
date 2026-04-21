from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from rest_framework import routers

from cart import views
from cart.views import CartItemViewSet, CartView

router = routers.DefaultRouter()
router.register(r'cartitem', CartItemViewSet)






urlpatterns = [
    path('', include(router.urls)),
    path('cart/my/', CartView.as_view({'get': 'my'}), name='cart-my'),  # добавить
    path('cart/', CartView.as_view({'get': 'retrieve'}), name='cart'),
]