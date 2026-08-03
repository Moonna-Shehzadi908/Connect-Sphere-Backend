from django.urls import path

from .views import (
    CreatePostView,
    PostListView,
    ToggleLikeView,
    DeletePostView,
    CommentView,
    DeleteCommentView,
)

urlpatterns = [

    # ==========================
    # Create Post
    # ==========================
    path(
        "",
        CreatePostView.as_view(),
        name="create-post",
    ),
    path(
    "<int:post_id>/delete/",
    DeletePostView.as_view(),
    name="delete-post",
),

    # ==========================
    # Feed
    # ==========================
    path(
        "feed/",
        PostListView.as_view(),
        name="post-feed",
    ),

    # ==========================
    # Like / Unlike
    # ==========================
    path(
        "<int:post_id>/like/",
        ToggleLikeView.as_view(),
        name="toggle-like",
    ),

    # ==========================
    # Add Comment
    # ==========================
    path(
        "<int:post_id>/comments/",
        CommentView.as_view(),
        name="post-comments",
    ),

    # ==========================
    # Delete Comment
    # ==========================
    path(
        "comments/<int:comment_id>/delete/",
        DeleteCommentView.as_view(),
        name="delete-comment",
    ),

]