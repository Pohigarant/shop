from django.shortcuts import render
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from review.models import Review
from review.serializers import ReviewSerializer
from shop1.permissions import IsOwnerOrAdmin


# Create your views here.
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter )
    filterset_fields = ('product__name',)   #для фильтрации по имени продукта
    search_fields = ('text', 'product__name')  # для поиска по тексту и по имени продукта
    ordering_fields = ('-created_at','rating') # поля для сортировки по дате осзданя и по рейтингу
    ordering = ('-created_at',)


    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Автоматически подставляем текущего пользователя
        serializer.save(user=self.request.user)