from django.db import models
from django.conf import settings


class Profile(models.Model):
    """
    Stores personal information about the user.

    Authentication remains inside the User model.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    bio = models.TextField(
        blank=True,
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    cover_photo = models.ImageField(
        upload_to="covers/",
        blank=True,
        null=True,
    )

    website = models.URLField(
        blank=True,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
    )

    is_private = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.user.username