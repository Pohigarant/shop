from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

from review.views import ReviewViewSet
from users.views import UserViewSet, LogoutView, UserRegisterView

router = routers.DefaultRouter()
router.register('users', UserViewSet)

user_register_router = NestedDefaultRouter(router, r'users', lookup='user')
user_register_router.register('reviews', ReviewViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('',include(user_register_router.urls)),

    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
]