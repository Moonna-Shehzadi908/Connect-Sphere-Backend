from django.urls import path

from .views import (
    CreatePostView,
    PostListView,
    ToggleLikeView,
)

urlpatterns = [

    path(
        "",
        CreatePostView.as_view(),
        name="create-post",
    ),

    path(
        "feed/",
        PostListView.as_view(),
        name="post-feed",
    ),

    path(
        "<int:post_id>/like/",
        ToggleLikeView.as_view(),
        name="toggle-like",
    ),

]