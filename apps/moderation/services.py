from .models import Report


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