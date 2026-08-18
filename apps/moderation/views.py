# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateReportSerializer
from .services import create_report
from rest_framework.generics import ListAPIView

from apps.core.pagination import DefaultPagination

from .permissions import IsModerator
from .selectors import get_reports
from .serializers import ReportListSerializer

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