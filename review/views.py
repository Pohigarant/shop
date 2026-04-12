from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from review.models import Review
from review.serializers import ReviewSerializer
from shop1.permissions import IsOwnerOrAdmin


# Create your views here.
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()