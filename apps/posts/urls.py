from django.urls import path

from .views import (
    ArchivePostView,
    CreatePostView,
    PinPostView,
    RestorePostView,
    TimelineView,
    PostDetailView,
    UnpinPostView,
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
    path(    
       "<int:post_id>/pin/",
       PinPostView.as_view(),
       name="pin-post",
    ),

    path(
        "<int:post_id>/unpin/",
        UnpinPostView.as_view(),
        name="unpin-post",
    ),

    path(
        "<int:post_id>/archive/",
        ArchivePostView.as_view(),
        name="archive-post",
    ),

    path(
        "<int:post_id>/restore/",
        RestorePostView.as_view(),
    name="restore-post",
    ),
]