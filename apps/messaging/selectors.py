from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django.db.models import Count, Max, Q
from .models import Conversation

User = get_user_model()


def get_user(user_id):
    """
    Return a user by ID.
    """

    return get_object_or_404(
        User,
        id=user_id,
    )

def get_user_conversations(user):

    return (
        Conversation.objects
        .filter(participants=user)
        .prefetch_related(
            "participants",
            "messages",
        )
        .annotate(
            last_activity=Max("messages__created_at"),
            unread_count=Count(
                "messages",
                filter=Q(
                    messages__is_read=False
                ) & ~Q(
                    messages__sender=user
                )
            ),
        )
        .order_by("-last_activity")
    )


def get_conversation(conversation_id):
    """
    Return a conversation by its ID.
    """

    return get_object_or_404(
        Conversation,
        id=conversation_id,
    )

from .models import Message


def get_conversation_messages(conversation):
    """
    Return all messages for a conversation.
    """

    return (
        Message.objects
        .filter(conversation=conversation)
        .select_related("sender")
        .order_by("created_at")
    )

def get_total_unread_messages(user):

    return (
        Message.objects
        .filter(
            conversation__participants=user,
            is_read=False,
        )
        .exclude(
            sender=user,
        )
        .count()
    )


def get_message(message_id):
    """
    Return a message by ID.
    """

    return get_object_or_404(
        Message,
        id=message_id,
    )

def search_messages(user, query):
    """
    Search messages belonging to conversations
    that the authenticated user participates in.
    """

    return (
        Message.objects
        .filter(
            conversation__participants=user,
            is_deleted=False,
        )
        .filter(
            Q(content__icontains=query)
        )
        .select_related(
            "sender",
            "conversation",
        )
        .distinct()
        .order_by("-created_at")
    )