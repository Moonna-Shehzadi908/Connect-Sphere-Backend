from django.urls import path

from .views import (
    CreatePostView,
    TimelineView,
    PostDetailView,
    UserPostsView,
    UpdatePostView,
    DeletePostView,
)


urlpatterns = [

    path(
        "",
        TimelineView.as_view(),
        name="timeline",
    ),

    path(
        "create/",
        CreatePostView.as_view(),
        name="create-post",
    ),

    path(
        "<int:post_id>/",
        PostDetailView.as_view(),
        name="post-detail",
    ),

    path(
        "user/<str:username>/",
        UserPostsView.as_view(),
        name="user-posts",
    ),
    path(
       "<int:post_id>/update/",
        UpdatePostView.as_view(),
        name="update-post",
    ),

    path(
        "<int:post_id>/delete/",
        DeletePostView.as_view(),
        name="delete-post",
    ),
]