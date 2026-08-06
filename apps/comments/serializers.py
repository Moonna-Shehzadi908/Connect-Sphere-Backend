from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    class Meta:

        model = Comment

        fields = (
            "id",
            "author",
            "post",
            "parent",
            "content",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "author",
            "created_at",
            "updated_at",
        ) 