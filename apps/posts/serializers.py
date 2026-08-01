from rest_framework import serializers

from .models import (
    Post,
    PostImage,
    PostLike,
    Comment,
)


# ==========================
# POST IMAGE
# ==========================

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = (
            "id",
            "image",
        )


# ==========================
# COMMENT
# ==========================

class CommentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    avatar = serializers.ImageField(
        source="author.profile.avatar",
        read_only=True,
    )

    class Meta:
        model = Comment

        fields = (
            "id",
            "username",
            "avatar",
            "content",
            "is_edited",
            "created_at",
        )

        read_only_fields = (
            "id",
            "username",
            "avatar",
            "is_edited",
            "created_at",
        )
# ==========================
# POST
# ==========================

class PostSerializer(serializers.ModelSerializer):

    images = PostImageSerializer(
        many=True,
        read_only=True,
    )

    comments = CommentSerializer(
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

    comments_count = serializers.SerializerMethodField()

    is_liked = serializers.SerializerMethodField()

    class Meta:

        model = Post

        fields = (
            "id",
            "username",
            "avatar",
            "likes_count",
            "comments_count",
            "is_liked",
            "content",
            "visibility",
            "images",
            "comments",
            "created_at",
            "updated_at",
        )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):

        request = self.context.get("request")

        if request and request.user.is_authenticated:

            return PostLike.objects.filter(
                post=obj,
                user=request.user,
            ).exists()

        return False