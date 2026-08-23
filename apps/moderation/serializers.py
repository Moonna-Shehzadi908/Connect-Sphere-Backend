from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import (
    Report,
    UserWarning,
)

from apps.posts.models import Post
from apps.comments.models import Comment


User = get_user_model()


# =========================================================
# CREATE REPORT
# =========================================================

class CreateReportSerializer(
    serializers.Serializer
):

    reported_user = (
        serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all(),
            required=False,
            allow_null=True,
        )
    )

    reported_post = (
        serializers.PrimaryKeyRelatedField(
            queryset=Post.objects.all(),
            required=False,
            allow_null=True,
        )
    )

    reported_comment = (
        serializers.PrimaryKeyRelatedField(
            queryset=Comment.objects.all(),
            required=False,
            allow_null=True,
        )
    )

    reason = serializers.ChoiceField(
        choices=Report.Reason.choices
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs):

        targets = [
            attrs.get("reported_user"),
            attrs.get("reported_post"),
            attrs.get("reported_comment"),
        ]

        if sum(
            target is not None
            for target in targets
        ) != 1:

            raise serializers.ValidationError(
                "Select exactly one object to report."
            )

        return attrs


# =========================================================
# REPORT LIST
# =========================================================

class ReportListSerializer(
    serializers.ModelSerializer
):

    reporter = serializers.CharField(
        source="reporter.username",
        read_only=True,
    )

    reviewed_by = serializers.CharField(
        source="reviewed_by.username",
        read_only=True,
    )

    class Meta:

        model = Report

        fields = (
            "id",
            "reporter",
            "reason",
            "status",
            "created_at",
            "reviewed_by",
        )


# =========================================================
# SIMPLE USER
# =========================================================

class SimpleUserSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = User

        fields = (
            "id",
            "username",
        )


# =========================================================
# SIMPLE POST
# =========================================================

class SimplePostSerializer(
    serializers.ModelSerializer
):

    author = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    class Meta:

        model = Post

        fields = (
            "id",
            "content",
            "author",
        )


# =========================================================
# SIMPLE COMMENT
# =========================================================

class SimpleCommentSerializer(
    serializers.ModelSerializer
):

    author = serializers.CharField(
        source="author.username",
        read_only=True,
    )

    class Meta:

        model = Comment

        fields = (
            "id",
            "content",
            "author",
        )


# =========================================================
# REPORT DETAIL
# =========================================================

class ReportDetailSerializer(
    serializers.ModelSerializer
):

    reporter = SimpleUserSerializer()

    reported_user = SimpleUserSerializer(
        allow_null=True,
    )

    reported_post = SimplePostSerializer(
        allow_null=True,
    )

    reported_comment = SimpleCommentSerializer(
        allow_null=True,
    )

    reviewed_by = SimpleUserSerializer(
        allow_null=True,
    )

    class Meta:

        model = Report

        fields = (
            "id",
            "reporter",
            "reported_user",
            "reported_post",
            "reported_comment",
            "reason",
            "description",
            "status",
            "reviewed_by",
            "review_note",
            "created_at",
            "reviewed_at",
        )


# =========================================================
# MODERATION ACTION
# =========================================================

class ModerationActionSerializer(
    serializers.Serializer
):

    action = serializers.ChoiceField(
        choices=[
            (
                "remove_post",
                "Remove Post",
            ),
            (
                "remove_comment",
                "Remove Comment",
            ),
            (
                "warn_user",
                "Warn User",
            ),
            (
                "suspend_user",
                "Suspend User",
            ),
            (
                "ban_user",
                "Ban User",
            ),
            (
                "restore_content",
                "Restore Content",
            ),
        ]
    )


# =========================================================
# MODERATION ANALYTICS
# =========================================================

class ModerationAnalyticsSerializer(
    serializers.Serializer
):

    reports_over_time = (
        serializers.ListField()
    )

    reports_by_reason = (
        serializers.ListField()
    )

    top_reporters = (
        serializers.ListField()
    )

    top_moderators = (
        serializers.ListField()
    )

    average_resolution_time = (
        serializers.CharField()
    )


# =========================================================
# USER WARNING
# =========================================================

class UserWarningSerializer(
    serializers.ModelSerializer
):

    moderator = serializers.CharField(
        source="moderator.username",
        read_only=True,
        allow_null=True,
    )

    reported_post_id = serializers.IntegerField(
        source="reported_post.id",
        read_only=True,
        allow_null=True,
    )

    class Meta:

        model = UserWarning

        fields = (
            "id",
            "reason",
            "moderator",
            "reported_post_id",
            "created_at",
        )