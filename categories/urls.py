from django.urls import include, path
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

from categories.views import CategoryViewSet
from products.views import ProductViewSet

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")

product_router = NestedDefaultRouter(router, r"categories", lookup="category")
product_router.register(
    r"products", ProductViewSet, basename="category-products"
)
urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
]
