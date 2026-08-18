# Create your models here.
from django.conf import settings
from django.db import models

from apps.posts.models import Post
from apps.comments.models import Comment


class Report(models.Model):

    class Reason(models.TextChoices):

        SPAM = "spam", "Spam"
        HARASSMENT = "harassment", "Harassment"
        HATE_SPEECH = "hate_speech", "Hate Speech"
        VIOLENCE = "violence", "Violence"
        MISINFORMATION = "misinformation", "False Information"
        NUDITY = "nudity", "Nudity"
        COPYRIGHT = "copyright", "Copyright"
        SCAM = "scam", "Scam"
        OTHER = "other", "Other"

    class Status(models.TextChoices):

        PENDING = "pending", "Pending"
        RESOLVED = "resolved", "Resolved"
        REJECTED = "rejected", "Rejected"

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_created",
    )

    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_received",
        null=True,
        blank=True,
    )

    reported_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    reported_comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    reason = models.CharField(
        max_length=30,
        choices=Reason.choices,
    )

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_reports",
    )

    review_note = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Report #{self.id} ({self.status})"