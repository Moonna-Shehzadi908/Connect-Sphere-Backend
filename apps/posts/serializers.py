from rest_framework import serializers

from .models import (
    Post,
    PostImage,
)


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = (
            "id",
            "image",
        )


class PostSerializer(serializers.ModelSerializer):

    images = PostImageSerializer(
        many=True,
        read_only=True,
    )

    # NEW FIELDS
    username = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    avatar = serializers.ImageField(
        source="author.profile.avatar",
        read_only=True,
    )

    class Meta:

        model = Post

        fields = (
            "id",
            "username",
            "avatar",
            "content",
            "visibility",
            "images",
            "created_at",
            "updated_at",
        )