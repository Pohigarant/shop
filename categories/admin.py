from typing import ClassVar

from django.contrib import admin

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {
        "slug": ("name",)
    }
    ordering = ("name",)
    list_editable = ("name",)
    list_per_page = 20
    search_fields = ("name",)
    list_filter = ("name",)
