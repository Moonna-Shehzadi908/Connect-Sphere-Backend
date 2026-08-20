# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateReportSerializer, ModerationAnalyticsSerializer
from .services import create_report
from rest_framework.generics import ListAPIView

from apps.core.pagination import DefaultPagination

from .permissions import IsModerator
from .selectors import get_average_resolution_time, get_report, get_reports, get_reports_over_time, get_top_moderators, get_top_reporters, get_reports_by_reason
from .serializers import ReportListSerializer
from rest_framework.generics import RetrieveAPIView

from .serializers import ReportDetailSerializer

from .services import perform_moderation_action
from .serializers import ModerationActionSerializer
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

class ReportListView(ListAPIView):

    permission_classes = [
        IsModerator
    ]

    serializer_class = ReportListSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):

        status = self.request.query_params.get(
            "status"
        )

        return get_reports(status)

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

class ModerationActionView(APIView):

    permission_classes = [
        IsModerator
    ]

    def post(
        self,
        request,
        report_id,
    ):

        report = get_report(report_id)

        serializer = ModerationActionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        perform_moderation_action(
            report=report,
            action=serializer.validated_data["action"],
        )

        return Response(
            {
                "message": "Moderation action completed."
            }
        )

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

            "top_reporters":[

                {
                    "id":u.id,
                    "username":u.username,
                    "reports_created":u.reports_created,
                }

                for u in get_top_reporters()

            ],

            "top_moderators":[

                {
                    "id":u.id,
                    "username":u.username,
                    "reviews":u.reviews,
                }

                for u in get_top_moderators()

            ],

            "average_resolution_time":

                str(

                    get_average_resolution_time()[
                        "average"
                    ]

                )

        }

        serializer = ModerationAnalyticsSerializer(data)

        return Response(serializer.data)