from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from products.filters import ProductFilter
from products.models import Product
from products.pagination import ProductPagination
from products.serializers import (
    ProductDetailSerializer,
    ProductListSerializer,
)


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    filterset_fields = ("category", "is_active")
    search_fields = ("name", "model", "article")
    ordering_fields = ("name", "model", "price", "quantity", "created_at")
    ordering = ("name",)

    def get_permissions(self):
        if self.action in ("list", "retrieve", "popular"):
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        category_pk = self.kwargs.get("category_pk")
        if category_pk:
            return Product.objects.filter(category_id=category_pk)
        return Product.objects.all()

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def popular(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.annotate(reviews_count=Count("reviews")).order_by(
            "-reviews_count"
        )[:5]
        serializer = ProductDetailSerializer(queryset, many=True)
        return Response(serializer.data)
