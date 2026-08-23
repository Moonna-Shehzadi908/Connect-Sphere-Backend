from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Conversation, Message

User = get_user_model()


class StartConversationSerializer(serializers.Serializer):

    participant_id = serializers.IntegerField()


class ConversationSerializer(serializers.ModelSerializer):

    participant = serializers.SerializerMethodField()

    last_message = serializers.SerializerMethodField()

    last_message_time = serializers.SerializerMethodField()

    unread_count = serializers.IntegerField(
        read_only=True
    )

    class Meta:

        model = Conversation

        fields = (
            "id",
            "participant",
            "last_message",
            "last_message_time",
            "unread_count",
        )

    def get_participant(self, obj):

        request = self.context["request"]

        other = obj.participants.exclude(
            id=request.user.id
        ).first()

        if other is None:
            return None

        avatar = None

        try:
            if hasattr(other, "profile") and other.profile.avatar:
                avatar = other.profile.avatar.url
        except Exception:
            avatar = None

        if avatar and request:
            avatar = request.build_absolute_uri(
                avatar
            )

        return {
            "id": other.id,
            "username": other.username,
            "avatar": avatar,
        }

    def get_last_message(self, obj):

        message = obj.messages.order_by(
            "-created_at"
        ).first()

        if not message:
            return ""

        if message.is_deleted:
            return "This message was deleted."

        return message.content

    def get_last_message_time(self, obj):

        message = obj.messages.order_by(
            "-created_at"
        ).first()

        return (
            message.created_at
            if message
            else None
        )


class SendMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            "conversation",
            "content",
            "attachment",
        )

    def validate(self, attrs):

        content = attrs.get("content")
        attachment = attrs.get("attachment")

        if not content and not attachment:
            raise serializers.ValidationError(
                "A message must contain text or an attachment."
            )

        return attrs


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField()

    content = serializers.SerializerMethodField()

    attachment = serializers.SerializerMethodField()

    class Meta:

        model = Message

        fields = (
            "id",
            "content",
            "sender",
            "attachment",
            "is_read",
            "created_at",
        )

    def get_content(self, obj):

        if obj.is_deleted:

            return "This message was deleted."

        return obj.content

    def get_sender(self, obj):

        avatar = None

        try:
            if hasattr(obj.sender, "profile") and obj.sender.profile.avatar:
                avatar = obj.sender.profile.avatar.url
        except Exception:
            avatar = None

        request = self.context.get("request")

        if avatar and request:
            avatar = request.build_absolute_uri(
                avatar
            )

        return {
            "id": obj.sender.id,
            "username": obj.sender.username,
            "avatar": avatar,
        }

    def get_attachment(self, obj):

        if obj.attachment:

            request = self.context.get("request")

            if request:

                return request.build_absolute_uri(
                    obj.attachment.url
                )

            return obj.attachment.url

        return None


class MessageSearchSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField()

    attachment = serializers.SerializerMethodField()

    class Meta:

        model = Message

        fields = (
            "id",
            "conversation",
            "sender",
            "content",
            "attachment",
            "created_at",
        )

    def get_sender(self, obj):

        avatar = None

        try:
            if hasattr(obj.sender, "profile") and obj.sender.profile.avatar:
                avatar = obj.sender.profile.avatar.url
        except Exception:
            avatar = None

        request = self.context.get("request")

        if avatar and request:
            avatar = request.build_absolute_uri(
                avatar
            )

        return {
            "id": obj.sender.id,
            "username": obj.sender.username,
            "avatar": avatar,
        }

    def get_attachment(self, obj):

        if obj.attachment:

            request = self.context.get("request")

            if request:

                return request.build_absolute_uri(
                    obj.attachment.url
                )

            return obj.attachment.url

        return None