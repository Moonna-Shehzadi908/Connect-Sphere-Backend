from django.urls import path

from .views import CreateCommentView

urlpatterns = [

    path(
        "",
        CreateCommentView.as_view(),
        name="create-comment",
    ),

]