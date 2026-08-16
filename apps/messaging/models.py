# Create your models here.
from django.conf import settings
from django.db import models


class Conversation(models.Model):
    """
    Represents a chat between two or more users.
    """

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ConversationParticipant",
        related_name="conversations",
    )

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Conversation {self.id}"

class ConversationParticipant(models.Model):
    """
    Stores users participating in a conversation.
    """

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="conversation_participants",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversation_participants",
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "conversation",
            "user",
        )

    def __str__(self):
        return f"{self.user.username} - {self.conversation.id}"

class Message(models.Model):
    """
    Represents a message inside a conversation.
    """

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )

    content = models.TextField()

    is_read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    is_deleted = models.BooleanField(
        default=False,
        )

    deleted_at = models.DateTimeField(
       null=True,
        blank=True,
    )
    attachment = models.FileField(
        upload_to="messages/",
        null=True,
        blank=True,
    )
    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message {self.id}"