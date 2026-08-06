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

from django.shortcuts import get_object_or_404
from .permissions import IsPostOwner
from .services import update_post
from .models import Post

class UpdatePostView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)

        self.check_object_permissions(request, post)

        content = request.data.get("content", post.content)

        visibility = request.data.get(
            "visibility",
            post.visibility,
        )

        post = update_post(
            post,
            content,
            visibility,
        )

        serializer = PostSerializer(post)

        return Response(serializer.data)

    def get_permissions(self):

        if self.request.method == "PUT":
            return [
                IsAuthenticated(),
                IsPostOwner(),
            ]

        return super().get_permissions()

from .services import delete_post
class DeletePostView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)

        self.check_object_permissions(request, post)

        delete_post(post)

        return Response(
            {
                "message": "Post deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    def get_permissions(self):

        if self.request.method == "DELETE":
            return [
                IsAuthenticated(),
                IsPostOwner(),
            ]

        return super().get_permissions()

from .services import (pin_post,unpin_post,archive_post,restore_post,)

class PinPostView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPostOwner,
    ]

    def post(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)

        self.check_object_permissions(request, post)

        pin_post(post)

        return Response({
            "message": "Post pinned successfully."
        })
    
class UnpinPostView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPostOwner,
    ]

    def post(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)

        self.check_object_permissions(request, post)

        unpin_post(post)

        return Response({
            "message": "Post unpinned successfully."
        })
class ArchivePostView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPostOwner,
    ]

    def post(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)

        self.check_object_permissions(request, post)

        archive_post(post)

        return Response({
            "message": "Post archived successfully."
        })

class RestorePostView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPostOwner,
    ]

    def post(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)

        self.check_object_permissions(request, post)

        restore_post(post)

        return Response({
            "message": "Post restored successfully."
        })