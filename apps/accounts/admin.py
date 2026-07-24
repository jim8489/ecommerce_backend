from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    ordering = ["email"]

    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = (

        (None, {

            "fields": (
                "email",
                "password",
            )

        }),

        ("Personal", {

            "fields": (
                "first_name",
                "last_name",
            )

        }),

        ("Permissions", {

            "fields": (

                "is_staff",

                "is_active",

                "is_superuser",

                "groups",

                "user_permissions",

            )

        }),

    )

    add_fieldsets = (

        (None, {

            "classes": ("wide",),

            "fields": (

                "email",

                "password1",

                "password2",

            ),

        }),

    )