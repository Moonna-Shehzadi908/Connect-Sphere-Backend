from .models import Report


def get_reports(status=None):

    queryset = (
        Report.objects
        .select_related(
            "reporter",
            "reported_user",
            "reviewed_by",
            "reported_post",
            "reported_comment",
        )
        .order_by("-created_at")
    )

    if status:

        queryset = queryset.filter(
            status=status
        )

    return queryset