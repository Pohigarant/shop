
from django.urls import path, include
from rest_framework import routers

from categories.views import CategoryViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)





urlpatterns = [
    path('', include(router.urls)),

]