from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from products.models import Product
from review.models import Review
from review.pagination import ReviewPagination
from review.serializers import ReviewSerializer
from shop1.permissions import HasPurchasedProduct, IsOwnerOrAdmin


# Create your views here.
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("product__name",)  # для фильтрации по имени продукта
    search_fields = (
        "text",
        "product__name",
    )  # для поиска по тексту и по имени продукта
    ordering_fields = (
        "created_at",
        "rating",
    )  # поля для сортировки по дате осзданя и по рейтингу
    ordering = ("-created_at",)

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        if self.action == "create":
            return [IsAuthenticated(), HasPurchasedProduct()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        product_pk = self.kwargs.get("prod_pk")
        user_pk = self.kwargs.get("user_pk")
        if product_pk:
            return Review.objects.filter(product_id=product_pk).select_related(
                "user", "product"
            )
        if user_pk:
            return Review.objects.filter(user_id=user_pk).select_related(
                "user", "product"
            )
        return Review.objects.all().select_related("user", "product")

    def perform_create(self, serializer):
        prod_pk = self.kwargs.get("prod_pk")
        if prod_pk:
            product = get_object_or_404(Product, pk=prod_pk)
            serializer.save(user=self.request.user, product=product)
        else:
            serializer.save(user=self.request.user)
