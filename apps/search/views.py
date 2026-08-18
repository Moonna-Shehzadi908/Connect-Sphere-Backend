# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.pagination import DefaultPagination

from .selectors import (get_posts_by_hashtag, get_trending_hashtags,
 search_users,search_posts,search_hashtags, get_search_suggestions,global_search)

from .serializers import (UserSearchSerializer,PostSearchSerializer,HashtagSearchSerializer,
    SearchSuggestionSerializer,GlobalSearchSerializer)


class UserSearchView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = UserSearchSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):

        query = self.request.query_params.get(
            "q",
            ""
        )

        return search_users(query)

class PostSearchView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = PostSearchSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):

        query = self.request.query_params.get(
            "q",
            ""
        )

        return search_posts(query)

class HashtagSearchView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = HashtagSearchSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):

        query = self.request.query_params.get(
            "q",
            ""
        )

        return search_hashtags(query)

class HashtagPostsView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = PostSearchSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):

        return get_posts_by_hashtag(
            self.kwargs["name"]
        )

class TrendingHashtagView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = HashtagSearchSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):

        return get_trending_hashtags()





class SearchSuggestionView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        query = request.query_params.get(
            "q",
            ""
        )

        suggestions = get_search_suggestions(
            query
        )

        serializer = SearchSuggestionSerializer(
            suggestions
        )

        return Response(serializer.data)

class GlobalSearchView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        query = request.query_params.get(
            "q",
            ""
        )

        results = global_search(query)

        serializer = GlobalSearchSerializer(
            results
        )

        return Response(
            serializer.data
        )