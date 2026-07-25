from rest_framework import serializers

from .models import Post, PostImage


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

    author = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    hashtags = serializers.SerializerMethodField()

    mentions = serializers.SerializerMethodField()

    class Meta:

        model = Post

        fields = (
            "id",
            "author",
            "content",
            "visibility",
            "hashtags",
            "mentions",
            "images",
            "created_at",
        )

    def get_hashtags(self, obj):
        return [tag.name for tag in obj.hashtags.all()]

    def get_mentions(self, obj):
        return [
            mention.user.username
            for mention in obj.mentions.all()
        ]