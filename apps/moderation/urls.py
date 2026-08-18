from django.urls import path

from .views import CreateReportView, ReportListView

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
]