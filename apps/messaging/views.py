from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from apps.core.pagination import DefaultPagination

from .models import Message

from .selectors import (
    get_message,
    get_total_unread_messages,
    get_user,
    get_user_conversations,
    get_conversation,
    get_conversation_messages,
)

from .serializers import (
    MessageSerializer,
    StartConversationSerializer,
    ConversationSerializer,
    SendMessageSerializer,
    MessageSearchSerializer,
)

from .services import (
    delete_message,
    get_or_create_conversation,
    send_message,
    mark_messages_as_read,
)

from .permissions import IsConversationParticipant

from .selectors import search_messages


class StartConversationView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = StartConversationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        participant = get_user(
            serializer.validated_data[
                "participant_id"
            ]
        )

        conversation = get_or_create_conversation(
            request.user,
            participant,
        )

        return Response(
            {
                "conversation_id": conversation.id
            },
            status=status.HTTP_201_CREATED,
        )


class ConversationListView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = ConversationSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):

        return get_user_conversations(
            self.request.user
        )


class SendMessageView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):

        serializer = SendMessageSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        conversation = get_conversation(
            serializer.validated_data[
                "conversation"
            ].id
        )

        permission = IsConversationParticipant()

        if not permission.has_object_permission(
            request,
            self,
            conversation,
        ):

            return Response(
                {
                    "detail":
                    "You are not a participant of this conversation."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        message = send_message(
            sender=request.user,
            conversation=conversation,
            content=serializer.validated_data.get(
                "content"
            ),
            attachment=serializer.validated_data.get(
                "attachment"
            ),
        )

        avatar = None

        try:

            if (
                hasattr(request.user, "profile")
                and request.user.profile.avatar
            ):

                avatar = (
                    request.user.profile.avatar.url
                )

        except Exception:

            avatar = None

        if avatar:

            avatar = request.build_absolute_uri(
                avatar
            )

        attachment = None

        if message.attachment:

            attachment = (
                request.build_absolute_uri(
                    message.attachment.url
                )
            )

        return Response(
            {
                "id": message.id,
                "conversation": conversation.id,

                "sender": {
                    "id": request.user.id,
                    "username":
                        request.user.username,
                    "avatar": avatar,
                },

                "content": (
                    "This message was deleted."
                    if message.is_deleted
                    else message.content
                ),

                "attachment": attachment,

                "is_read": message.is_read,

                "created_at":
                    message.created_at,
            },
            status=status.HTTP_201_CREATED,
        )


class MessageHistoryView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = MessageSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):

        conversation = get_conversation(
            self.kwargs[
                "conversation_id"
            ]
        )

        permission = IsConversationParticipant()

        if not permission.has_object_permission(
            self.request,
            self,
            conversation,
        ):

            return Message.objects.none()

        return get_conversation_messages(
            conversation
        )


class MarkConversationReadView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(
        self,
        request,
        conversation_id
    ):

        conversation = get_conversation(
            conversation_id
        )

        permission = IsConversationParticipant()

        if not permission.has_object_permission(
            request,
            self,
            conversation,
        ):

            return Response(
                {
                    "detail":
                    "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        updated = mark_messages_as_read(
            conversation,
            request.user,
        )

        return Response(
            {
                "messages_marked_read":
                    updated
            }
        )


class UnreadMessageCountView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        return Response(
            {
                "unread_messages":
                    get_total_unread_messages(
                        request.user
                    )
            }
        )


class DeleteMessageView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(
        self,
        request,
        message_id
    ):

        message = get_message(
            message_id
        )

        if message.sender != request.user:

            return Response(
                {
                    "detail":
                    "You can only delete your own messages."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        delete_message(
            message
        )

        return Response(
            {
                "message":
                    "Message deleted successfully."
            },
            status=status.HTTP_200_OK,
        )


class MessageSearchView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = MessageSearchSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):

        query = self.request.query_params.get(
            "q",
            ""
        )

        return search_messages(
            self.request.user,
            query,
        )