from django.urls import path

from .views import (GlobalSearchView, HashtagPostsView, HashtagSearchView, UserSearchView,
    PostSearchView, TrendingHashtagView, SearchSuggestionView)

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

    path(
        "hashtags/",
        HashtagSearchView.as_view(),
        name="search-hashtags",
    ),
    path(
        "hashtags/<str:name>/posts/",
        HashtagPostsView.as_view(),
        name="hashtag-posts",
    ),
    path(
        "trending-hashtags/",
        TrendingHashtagView.as_view(),
        name="trending-hashtags",
    ),
    path(
        "suggestions/",
        SearchSuggestionView.as_view(),
        name="search-suggestions",
    ),
    path(
        "",
        GlobalSearchView.as_view(),
        name="global-search",
    ),
]