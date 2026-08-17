from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )

from apps.posts.models import Post


class PostSearchSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:

        model = Post

        fields = (
            "id",
            "author",
            "content",
            "created_at",
        )

    def get_author(self, obj):

        return {
            "id": obj.author.id,
            "username": obj.author.username,
        }