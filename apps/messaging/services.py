from django.db import transaction
from .models import Conversation, ConversationParticipant, Message
from django.shortcuts import get_object_or_404

@transaction.atomic
def send_message(
    *,
    sender,
    conversation,
    content,
    attachment=None,
):
    return Message.objects.create(
        sender=sender,
        conversation=conversation,
        content=content,
        attachment=attachment,
    )

@transaction.atomic
def get_or_create_conversation(user1, user2):
    """
    Return an existing one-to-one conversation
    or create a new one.
    """

    if user1 == user2:
        raise ValueError(
            "You cannot start a conversation with yourself."
        )

    conversations = (
        Conversation.objects.filter(
            participants=user1
        ).filter(
            participants=user2
        )
    )

    for conversation in conversations:
        if conversation.participants.count() == 2:
            return conversation

    conversation = Conversation.objects.create()

    ConversationParticipant.objects.bulk_create([
        ConversationParticipant(
            conversation=conversation,
            user=user1,
        ),
        ConversationParticipant(
            conversation=conversation,
            user=user2,
        ),
    ])

    return conversation




def get_conversation(conversation_id):
    """
    Return a conversation by its ID.
    """

    return get_object_or_404(
        Conversation,
        id=conversation_id,
    )



def mark_messages_as_read(conversation, user):
    """
    Mark all unread messages in a conversation as read,
    excluding messages sent by the current user.
    """

    return (
        Message.objects
        .filter(
            conversation=conversation,
            is_read=False,
        )
        .exclude(
            sender=user,
        )
        .update(
            is_read=True,
        )
    )

from django.utils import timezone


def delete_message(message):
    """
    Soft delete a message.
    """

    message.is_deleted = True
    message.deleted_at = timezone.now()
    message.content = "This message was deleted."

    message.save(
        update_fields=[
            "is_deleted",
            "deleted_at",
            "content",
        ]
    )

    return message