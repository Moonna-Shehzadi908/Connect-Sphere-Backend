from datetime import timedelta
from enum import Enum

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Report, UserWarning


User = get_user_model()


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
    Create a new report.

    If the same reporter has an already-pending report
    for the same target, return that existing pending report.

    If the old report was resolved/rejected, create a
    fresh pending report.
    """

    existing_report = Report.objects.filter(
        reporter=reporter,
        reported_user=reported_user,
        reported_post=reported_post,
        reported_comment=reported_comment,
        status=Report.Status.PENDING,
    ).first()

    # Already reported and still pending
    if existing_report:
        return existing_report

    # Old report was resolved/rejected, so create a new one
    return Report.objects.create(
        reporter=reporter,
        reported_user=reported_user,
        reported_post=reported_post,
        reported_comment=reported_comment,
        reason=reason,
        description=description,
        status=Report.Status.PENDING,
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

def perform_moderation_action(
    *,
    report,
    action,
    moderator,
):

    # =====================================================
    # REMOVE POST
    # =====================================================

    if action == ModerationAction.REMOVE_POST.value:

        if not report.reported_post:
            raise ValidationError(
                "This report does not reference a post."
            )

        report.reported_post.delete()

        return


    # =====================================================
    # REMOVE COMMENT
    # =====================================================

    if action == ModerationAction.REMOVE_COMMENT.value:

        if not report.reported_comment:
            raise ValidationError(
                "This report does not reference a comment."
            )

        report.reported_comment.delete()

        return


    # =====================================================
    # WARN USER
    # =====================================================

    if action == ModerationAction.WARN_USER.value:

        user = get_reported_user(report)

        if not user:
            raise ValidationError(
                "No user found for this report."
            )

        UserWarning.objects.create(
            user=user,
            moderator=moderator,
            reported_post=report.reported_post,
            reason=report.reason,
        )

        return


    # =====================================================
    # SUSPEND USER
    # =====================================================

    if action == ModerationAction.SUSPEND_USER.value:

        user = get_reported_user(report)

        if not user:
            raise ValidationError(
                "No user found for this report."
            )

        user.is_suspended = True

        user.suspended_until = (
            timezone.now()
            + timedelta(days=7)
        )

        user.save()

        return


    # =====================================================
    # BAN USER
    # =====================================================

    if action == ModerationAction.BAN_USER.value:

        user = get_reported_user(report)

        if not user:
            raise ValidationError(
                "No user found for this report."
            )

        user.is_active = False
        user.save()

        return


    # =====================================================
    # RESTORE CONTENT
    # =====================================================

    if action == ModerationAction.RESTORE_CONTENT.value:

        raise ValidationError(
            "Restore content is not supported for permanently deleted content."
        )


    # =====================================================
    # INVALID ACTION
    # =====================================================

    raise ValidationError(
        "Invalid moderation action."
    )