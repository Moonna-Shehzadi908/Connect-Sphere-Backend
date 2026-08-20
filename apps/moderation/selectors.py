from .models import Report
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.contrib.auth import get_user_model

User = get_user_model()

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

def get_reports_over_time():

    return (

        Report.objects

        .annotate(
            day=TruncDate("created_at")
        )

        .values("day")

        .annotate(
            reports=Count("id")
        )

        .order_by("day")

    )

def get_top_reporters():

    return (

        User.objects

        .annotate(

            reports_created=Count(
                "reports_created"
            )

        )

        .order_by(
            "-reports_created"
        )[:10]

    )

def get_top_moderators():

    return (

        User.objects

        .annotate(

            reviews=Count(
                "reviewed_reports"
            )

        )

        .order_by(
            "-reviews"
        )[:10]

    )

from django.db.models import F, ExpressionWrapper
from django.db.models import DurationField
from django.db.models import Avg


def get_average_resolution_time():

    return (

        Report.objects

        .exclude(
            reviewed_at=None
        )

        .annotate(

            resolution_time=

            ExpressionWrapper(

                F("reviewed_at") - F("created_at"),

                output_field=DurationField(),

            )

        )

        .aggregate(

            average=Avg("resolution_time")

        )

    )

def get_reports_by_reason():
    
    return (

        Report.objects

        .values("reason")

        .annotate(
            reports=Count("id")
        )

        .order_by("-reports")

    )