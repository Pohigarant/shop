from typing import ClassVar, Sequence

from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "quantity",
        "is_active",
        "product_info",
        "created_at",
        "updated_at",
        "category",
        "slug"
    )
    list_display_links = ("id", "name", "slug")
    ordering = ("name", "created_at")
    prepopulated_fields: ClassVar[dict[str, Sequence[str]]] = {
        "slug": ("name",)
    }
    list_editable = ("is_active", "price", "product_info")
    list_per_page = 20
    list_filter = (
        "price",
        "quantity",
        "is_active",
        "created_at",
        "category_id",
    )
    search_fields = ("name", "slug", "article")
