from django.contrib import admin

from cart.models import CartItem, Cart


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','created_at','updated_at']
    ordering = ('-created_at',)
    list_per_page = 20



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity']
    ordering = ('quantity',)
    list_per_page = 20

