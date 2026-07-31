from rest_framework import serializers

from .models import (
    Post,
    PostImage,
    PostLike,
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

    username = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    avatar = serializers.ImageField(
        source="author.profile.avatar",
        read_only=True,
    )

    likes_count = serializers.SerializerMethodField()

    is_liked = serializers.SerializerMethodField()

    class Meta:

        model = Post

        fields = (
            "id",
            "username",
            "avatar",
            "likes_count",
            "is_liked",
            "content",
            "visibility",
            "images",
            "created_at",
            "updated_at",
        )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):

        request = self.context.get("request")

        if request and request.user.is_authenticated:

            return PostLike.objects.filter(
                post=obj,
                user=request.user,
            ).exists()

        return False