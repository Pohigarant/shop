from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from categories.models import Category
from categories.serializers import CategorySerializer

CACHE_KEY_CATEGORY = "categories:list:v1"


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)

    search_fields = ("name", "slug")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAdminUser()]

    def list(self, request, *args, **kwargs):
        data = cache.get(CACHE_KEY_CATEGORY)
        if data is None:
            response = super().list(request, *args, **kwargs)
            data = response.data
            cache.set(CACHE_KEY_CATEGORY, data, timeout=60)
        return Response(data)
