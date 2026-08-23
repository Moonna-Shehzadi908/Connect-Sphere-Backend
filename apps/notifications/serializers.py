from rest_framework import serializers

from .models import Notification


class NotificationSenderSerializer(serializers.Serializer):

    id = serializers.IntegerField()

    username = serializers.CharField()

    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):

        profile = getattr(
            obj,
            "profile",
            None,
        )

        if profile and profile.avatar:

            request = self.context.get(
                "request"
            )

            if request:

                return request.build_absolute_uri(
                    profile.avatar.url
                )

            return profile.avatar.url

        return None


class NotificationSerializer(
    serializers.ModelSerializer
):

    sender = NotificationSenderSerializer(
        read_only=True
    )

    class Meta:

        model = Notification

        fields = [
            "id",
            "sender",
            "notification_type",
            "message",
            "is_read",
            "created_at",
        ]