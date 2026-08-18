from django.urls import path

from .views import CreateReportView, ReportDetailView, ReportListView

urlpatterns = [

    path(
        "reports/",
        ReportListView.as_view(),
        name="reports-list",
    ),

    path(
        "reports/create/",
        CreateReportView.as_view(),
        name="create-report",
    ),
    path(
        "reports/<int:report_id>/",
        ReportDetailView.as_view(),
        name="report-detail",
    ),
]