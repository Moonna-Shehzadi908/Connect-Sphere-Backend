from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            "bio",
            "website",
            "location",
            "birth_date",
            "avatar",
            "cover_photo",
            "is_private",
        )

class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            "avatar",
        )

class CoverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            "cover_photo",
        )