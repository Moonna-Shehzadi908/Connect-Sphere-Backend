from .models import Report
from django.shortcuts import get_object_or_404
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




def get_report(report_id):

    return get_object_or_404(
        Report.objects.select_related(
            "reporter",
            "reported_user",
            "reported_post__author",
            "reported_comment__author",
            "reviewed_by",
        ),
        id=report_id,
    )