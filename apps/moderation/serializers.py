from rest_framework import serializers

from .models import Report
from apps.posts.models import Post
from apps.comments.models import Comment
from django.contrib.auth import get_user_model
from apps.posts.models import Post
from apps.comments.models import Comment

User = get_user_model()


class CreateReportSerializer(serializers.Serializer):

    reported_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    reported_post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        required=False,
        allow_null=True,
    )

    reported_comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        required=False,
        allow_null=True,
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

        if sum(target is not None for target in targets) != 1:

            raise serializers.ValidationError(
                "Select exactly one object to report."
            )

        return attrs

class ReportListSerializer(serializers.ModelSerializer):

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

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = (
            "id",
            "username",
        )


class SimplePostSerializer(serializers.ModelSerializer):

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

class SimpleCommentSerializer(serializers.ModelSerializer):

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

class ReportDetailSerializer(serializers.ModelSerializer):

    reporter = SimpleUserSerializer()

    reported_user = SimpleUserSerializer()

    reported_post = SimplePostSerializer()

    reported_comment = SimpleCommentSerializer()

    reviewed_by = SimpleUserSerializer()

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