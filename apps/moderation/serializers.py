from rest_framework import serializers

from .models import Report
from apps.posts.models import Post
from apps.comments.models import Comment
from django.contrib.auth import get_user_model

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