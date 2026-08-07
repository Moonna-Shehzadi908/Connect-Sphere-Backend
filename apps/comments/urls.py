from django.urls import path

from .views import (
    CreateCommentView,
    DeleteCommentView,
)


urlpatterns = [

    path(
        "",
        CreateCommentView.as_view(),
        name="create-comment",
    ),

    path(
        "<int:comment_id>/delete/",
        DeleteCommentView.as_view(),
        name="delete-comment",
    ),

]