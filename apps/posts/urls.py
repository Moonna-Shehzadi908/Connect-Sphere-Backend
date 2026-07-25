from django.urls import path

from .views import (
    CreatePostView,
    PostListView,
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

]