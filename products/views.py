

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser

from products.filters import ProductFilter
from products.models import Product
from products.serializers import ProductSerializer, ProductListSerializer, ProductDetailSerializer


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = (ProductSerializer, ProductListSerializer, ProductDetailSerializer)

    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    # filterset_fields = ('category' 'is_active')
    search_fields = ('name', 'model', 'article')
    ordering_fields = ('name', 'model', 'price', 'quantity', 'created_at')
    ordering = ('name',)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [AllowAny()]
        return [IsAdminUser()]


    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer



