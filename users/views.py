from django.shortcuts import render
from rest_framework import viewsets, request
from rest_framework.permissions import IsAuthenticated

from shop1.permissions import IsOwnerOrAdmin
from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        if self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.none()
