# Create your views here.

from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.core.pagination import DefaultPagination

from .models import UserWarning

from .permissions import IsModerator

from .selectors import (
    get_average_resolution_time,
    get_report,
    get_reports,
    get_reports_over_time,
    get_top_moderators,
    get_top_reporters,
    get_reports_by_reason,
)

from .serializers import (
    CreateReportSerializer,
    ModerationAnalyticsSerializer,
    ReportListSerializer,
    ReportDetailSerializer,
    ModerationActionSerializer,
    UserWarningSerializer,
)

from .services import (
    create_report,
    perform_moderation_action,
)


# =========================================================
# CREATE REPORT
# =========================================================

class CreateReportView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = CreateReportSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        report = create_report(
            reporter=request.user,
            **serializer.validated_data,
        )

        return Response(
            {
                "message": "Report submitted successfully.",
                "report_id": report.id,
                "status": report.status,
            },
            status=status.HTTP_201_CREATED,
        )


# =========================================================
# REPORT LIST
# =========================================================

class ReportListView(ListAPIView):

    permission_classes = [
        IsModerator
    ]

    serializer_class = ReportListSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):

        report_status = self.request.query_params.get(
            "status"
        )

        return get_reports(report_status)


# =========================================================
# REPORT DETAIL
# =========================================================

class ReportDetailView(RetrieveAPIView):

    permission_classes = [
        IsModerator
    ]

    serializer_class = ReportDetailSerializer

    lookup_url_kwarg = "report_id"

    def get_object(self):

        return get_report(
            self.kwargs["report_id"]
        )


# =========================================================
# MODERATION ACTION
# =========================================================

class ModerationActionView(APIView):

    permission_classes = [
        IsModerator
    ]

    def post(
        self,
        request,
        report_id,
    ):

        report = get_report(
            report_id
        )

        serializer = ModerationActionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        action = serializer.validated_data[
            "action"
        ]

        # =================================================
        # SAVE MODERATOR
        # =================================================

        report.reviewed_by = request.user
        report.reviewed_at = timezone.now()

        report.save(
            update_fields=[
                "reviewed_by",
                "reviewed_at",
            ]
        )

        # =================================================
        # PERFORM ACTION
        # =================================================

        perform_moderation_action(
            report=report,
            action=action,
            moderator=request.user,
        )

        # =================================================
        # UPDATE REPORT STATUS
        # =================================================

        if action in [
            "remove_post",
            "remove_comment",
            "warn_user",
            "suspend_user",
            "ban_user",
        ]:

            report.status = (
                report.Status.RESOLVED
            )

        elif action == "restore_content":

            report.status = (
                report.Status.REJECTED
            )

        report.save(
            update_fields=[
                "status",
            ]
        )

        return Response(
            {
                "message": (
                    "Moderation action completed."
                ),
                "status": report.status,
            },
            status=status.HTTP_200_OK,
        )


# =========================================================
# MODERATION ANALYTICS
# =========================================================

class ModerationAnalyticsView(APIView):

    permission_classes = [
        IsModerator
    ]

    def get(self, request):

        data = {

            "reports_over_time":
                list(
                    get_reports_over_time()
                ),

            "reports_by_reason":
                list(
                    get_reports_by_reason()
                ),

            "top_reporters": [

                {
                    "id": user.id,
                    "username": user.username,
                    "reports_created": (
                        user.reports_created
                    ),
                }

                for user in get_top_reporters()
            ],

            "top_moderators": [

                {
                    "id": user.id,
                    "username": user.username,
                    "reviews": user.reviews,
                }

                for user in get_top_moderators()
            ],

            "average_resolution_time":
                str(
                    get_average_resolution_time()[
                        "average"
                    ]
                ),
        }

        serializer = ModerationAnalyticsSerializer(
            data
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# =========================================================
# MY WARNINGS
# =========================================================

class MyWarningsView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        warnings = (
            UserWarning.objects
            .filter(
                user=request.user
            )
            .select_related(
                "moderator"
            )
            .order_by(
                "-created_at"
            )
        )

        serializer = UserWarningSerializer(
            warnings,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )