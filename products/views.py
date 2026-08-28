from django.db.models import Avg
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
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
    # filterset_fields = ("category", "is_active")
    search_fields = ("name", "model", "article")
    ordering_fields = ("name", "model", "price", "quantity", "created_at")
    ordering = ("name",)
    throttle_scope = "product_search"
    lookup_field = "slug"

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
        queryset = Product.objects.select_related("category").annotate(
            reviews_count=Count("reviews", distinct=True),
            average_rating=Avg("reviews__rating"),
        )

        return queryset

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def popular(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.order_by("-average_rating")[:5]
        serializer = ProductDetailSerializer(queryset, many=True)
        return Response(serializer.data)
