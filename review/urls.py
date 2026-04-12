from django.urls import path, include
from rest_framework import routers

from review.views import ReviewViewSet

router = routers.DefaultRouter()
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
