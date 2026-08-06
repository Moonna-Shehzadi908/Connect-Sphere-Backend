from django.urls import path

from .views import (
    CreatePostView,
    PostListView,
    ToggleLikeView,
    DeletePostView,
    CommentView,
    DeleteCommentView,
    TimelineView,
    PostDetailView,
    UserPostsView,
    UpdatePostView,
    PinPostView,
    UnpinPostView,
    ArchivePostView,
    RestorePostView,
)

urlpatterns = [

    # Timeline
    path(
        "",
        TimelineView.as_view(),
        name="timeline",
    ),

    # Create Post
    path(
        "create/",
        CreatePostView.as_view(),
        name="create-post",
    ),

    # Feed
    path(
        "feed/",
        PostListView.as_view(),
        name="post-feed",
    ),

    # Single Post
    path(
        "<int:post_id>/",
        PostDetailView.as_view(),
        name="post-detail",
    ),

    # User Posts
    path(
        "user/<str:username>/",
        UserPostsView.as_view(),
        name="user-posts",
    ),

    # Update Post
    path(
        "<int:post_id>/update/",
        UpdatePostView.as_view(),
        name="update-post",
    ),

    # Delete Post
    path(
        "<int:post_id>/delete/",
        DeletePostView.as_view(),
        name="delete-post",
    ),

    # Like
    path(
        "<int:post_id>/like/",
        ToggleLikeView.as_view(),
        name="toggle-like",
    ),

    # Comments
    path(
        "<int:post_id>/comments/",
        CommentView.as_view(),
        name="post-comments",
    ),

    # Delete Comment
    path(
        "comments/<int:comment_id>/delete/",
        DeleteCommentView.as_view(),
        name="delete-comment",
    ),

    # Pin
    path(
        "<int:post_id>/pin/",
        PinPostView.as_view(),
        name="pin-post",
    ),

    # Unpin
    path(
        "<int:post_id>/unpin/",
        UnpinPostView.as_view(),
        name="unpin-post",
    ),

    # Archive
    path(
        "<int:post_id>/archive/",
        ArchivePostView.as_view(),
        name="archive-post",
    ),

    # Restore
    path(
        "<int:post_id>/restore/",
        RestorePostView.as_view(),
        name="restore-post",
    ),
]