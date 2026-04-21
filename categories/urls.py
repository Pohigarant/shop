from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from rest_framework import routers

from categories.views import CategoryViewSet
from products.views import ProductViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)

product_router = NestedDefaultRouter(router, r'categories', lookup='category')
product_router.register('products', ProductViewSet, basename= 'category-products')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
]


