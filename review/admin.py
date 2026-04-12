from django.contrib import admin

from review.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['rating','text','created_at','product__name','user__email']
    ordering = ['rating']

    list_per_page = 20
    search_fields = ['rating']
    list_filter = ['rating']
