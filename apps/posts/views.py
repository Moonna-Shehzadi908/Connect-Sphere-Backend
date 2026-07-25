from rest_framework import status
from rest_framework.parsers import (FormParser,MultiPartParser,)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CS_backend.apps.posts.models import Post

from .serializers import PostSerializer
from .services import create_post

from django.http import Http404
from rest_framework.generics import ListAPIView

from .selectors import (
    get_post,
    get_timeline,
    get_user_posts,
)

class CreatePostView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def post(self, request):

        content = request.data.get(
            "content",
            "",
        )

        visibility = request.data.get(
            "visibility",
            "PUBLIC",
        )

        images = request.FILES.getlist(
            "images"
        )

        post = create_post(
            author=request.user,
            content=content,
            visibility=visibility,
            images=images,
        )

        serializer = PostSerializer(post)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
from apps.core.pagination import DefaultPagination
class TimelineView(ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer
    pagination_class = DefaultPagination
    def get_queryset(self):
        return get_timeline()


class PostDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):

        try:
            post = get_post(post_id)

        except Post.DoesNotExist:
            raise Http404("Post not found.")

        serializer = PostSerializer(post)

        return Response(serializer.data)

class UserPostsView(ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):

        username = self.kwargs["username"]

        return get_user_posts(username)

