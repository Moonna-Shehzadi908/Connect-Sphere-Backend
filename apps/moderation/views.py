# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateReportSerializer
from .services import create_report


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