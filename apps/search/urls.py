from django.urls import path

from .views import UserSearchView, PostSearchView

urlpatterns = [

    path(
        "users/",
        UserSearchView.as_view(),
        name="search-users",
    ),

    path(
        "posts/",
        PostSearchView.as_view(),
        name="search-posts",
    ),
]