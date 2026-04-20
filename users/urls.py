from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet, LogoutView, UserRegisterView

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('',include(router.urls)),

    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
]