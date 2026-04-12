from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny, IsAdminUser

from products.models import Product
from products.serializers import ProductSerializer


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAdminUser()]
