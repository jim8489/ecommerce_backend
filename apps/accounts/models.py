from django.db import models

from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
)

from .managers import UserManager


class User(
    AbstractBaseUser,
    PermissionsMixin,
):

    email = models.EmailField(
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    class Meta:

        db_table = "users"

        ordering = ["-created_at"]

    def __str__(self):

        return self.email