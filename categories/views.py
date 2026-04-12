from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAdminUser()]