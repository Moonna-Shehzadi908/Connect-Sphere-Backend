from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = "user", "User"
        MODERATOR = "moderator", "Moderator"
        ADMIN = "admin", "Admin"

    email = models.EmailField(
        unique=True
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username"
    ]

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    is_suspended = models.BooleanField(
        default=False,
    )

    suspended_until = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.email