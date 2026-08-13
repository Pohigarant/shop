from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class BuyerAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "phone",
        "city",
        "is_staff",
        "birth_date",
    )
