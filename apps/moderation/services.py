from django.contrib.admin import action

from .models import Report

from enum import Enum
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError

class ModerationAction(Enum):

    REMOVE_POST = "remove_post"

    REMOVE_COMMENT = "remove_comment"

    WARN_USER = "warn_user"

    SUSPEND_USER = "suspend_user"

    BAN_USER = "ban_user"

    RESTORE_CONTENT = "restore_content"
def create_report(
    *,
    reporter,
    reported_user=None,
    reported_post=None,
    reported_comment=None,
    reason,
    description="",
):
    """
    Create a report if one doesn't already exist
    for the same reporter and target.
    """

    report, created = Report.objects.get_or_create(
        reporter=reporter,
        reported_user=reported_user,
        reported_post=reported_post,
        reported_comment=reported_comment,
        defaults={
            "reason": reason,
            "description": description,
        },
    )

    return report


def get_reported_user(report):

    if report.reported_user:
        return report.reported_user

    if report.reported_post:
        return report.reported_post.author

    if report.reported_comment:
        return report.reported_comment.author

    return None

def perform_moderation_action(*,report, action,):
    if action == ModerationAction.REMOVE_POST.value:

        if not report.reported_post:
            raise ValidationError(
                "This report does not reference a post."
            )

        report.reported_post.is_deleted = True

        report.reported_post.save()

        return
    if action == ModerationAction.REMOVE_COMMENT.value:

        if not report.reported_comment:
            raise ValidationError(
                "This report does not reference a comment."
            )

        report.reported_comment.is_deleted = True

        report.reported_comment.save()

        return  
    if action == ModerationAction.WARN_USER.value:

        user = report.reported_user

        if not user and report.reported_post:
            user = report.reported_post.author

        if not user and report.reported_comment:
            user = report.reported_comment.author

        UserWarning.objects.create(
            user=user,
            moderator=report.reviewed_by,
            reason=report.reason,
        )

        return
    
    if action == ModerationAction.SUSPEND_USER.value:

        user = get_reported_user(report)

        user.is_suspended = True

        user.suspended_until = (
            timezone.now() + timedelta(days=7)
    )

        user.save()

        return