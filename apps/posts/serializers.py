import re

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

    class Meta:

        model = Post

        fields = (
            "id",
            "content",
            "visibility",
            "images",
            "created_at",
            "updated_at",
        )