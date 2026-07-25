from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Follow

User = get_user_model()


class FollowUserSerializer(serializers.ModelSerializer):
    """
    Serializer used to return information
    about the user being followed.
    """

    username = serializers.CharField(
        source="following.username",
        read_only=True,
    )

    class Meta:
        model = Follow
        fields = (
            "id",
            "username",
            "created_at",
        )

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserFollowerSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar",
        )

    def get_avatar(self, obj):
        if hasattr(obj, "profile") and obj.profile.avatar:
            return obj.profile.avatar.url
        return None