# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.core.pagination import DefaultPagination

from .selectors import (search_users,search_posts,)

from .serializers import (UserSearchSerializer,PostSearchSerializer,)

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