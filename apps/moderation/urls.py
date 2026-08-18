from django.urls import path

from .views import CreateReportView

urlpatterns = [

    path(
        "reports/",
        CreateReportView.as_view(),
        name="create-report",
    ),

]