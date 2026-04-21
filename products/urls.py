from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from products.views import ProductViewSet
from review.views import ReviewViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)

review_router = NestedDefaultRouter(router, r'products', lookup='prod')
review_router.register(r'reviews', ReviewViewSet, basename = "product-review")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(review_router.urls)),
]