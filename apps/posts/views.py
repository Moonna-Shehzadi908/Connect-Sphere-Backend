from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import status
from rest_framework.parsers import (
    JSONParser,
    MultiPartParser,
    FormParser,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from apps.core.pagination import DefaultPagination

from .models import (
    Post,
    PostLike,
    Comment,
)

from .serializers import (
    PostSerializer,
    CommentSerializer,
)

from .permissions import IsPostOwner

from .selectors import (
    get_post,
    get_timeline,
    get_user_posts,
)

from .services import (
    create_post,
    update_post,
    delete_post,
    pin_post,
    unpin_post,
    archive_post,
    restore_post,
)


# ==========================================================
# CREATE POST
# ==========================================================

class CreatePostView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = (
        JSONParser,
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

        serializer = PostSerializer(
            post,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


# ==========================================================
# TIMELINE
# ==========================================================

class TimelineView(ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return get_timeline()

    def get_serializer_context(self):

        context = super().get_serializer_context()

        context["request"] = self.request

        return context


# ==========================================================
# FEED
# ==========================================================

class PostListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        posts = (
            Post.objects
            .select_related(
                "author",
                "author__profile",
            )
            .prefetch_related(
                "images",
                "likes",
                "comments",
                "comments__author",
                "comments__author__profile",
            )
            .order_by("-created_at")
        )

        serializer = PostSerializer(
            posts,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# ==========================================================
# POST DETAIL
# ==========================================================

class PostDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):

        try:

            post = get_post(post_id)

        except Post.DoesNotExist:

            raise Http404(
                "Post not found."
            )

        serializer = PostSerializer(
            post,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# ==========================================================
# USER POSTS
# ==========================================================

class UserPostsView(ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):

        username = self.kwargs["username"]

        return get_user_posts(username)

    def get_serializer_context(self):

        context = super().get_serializer_context()

        context["request"] = self.request

        return context


# ==========================================================
# LIKE / UNLIKE
# ==========================================================

class ToggleLikeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id,
        )

        like = PostLike.objects.filter(
            post=post,
            user=request.user,
        )

        if like.exists():

            like.delete()

            return Response(
                {
                    "liked": False,
                    "likes_count": post.likes.count(),
                },
                status=status.HTTP_200_OK,
            )

        PostLike.objects.create(
            post=post,
            user=request.user,
        )

        return Response(
            {
                "liked": True,
                "likes_count": post.likes.count(),
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# ADD COMMENT
# ==========================================================

class CommentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id,
        )

        serializer = CommentSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            post=post,
            author=request.user,
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


# ==========================================================
# DELETE COMMENT
# ==========================================================

class DeleteCommentView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):

        comment = get_object_or_404(
            Comment,
            id=comment_id,
            author=request.user,
        )

        comment.delete()

        return Response(
            {
                "message": "Comment deleted."
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# UPDATE POST
# ==========================================================

class UpdatePostView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPostOwner,
    ]

    def put(self, request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id,
        )

        self.check_object_permissions(
            request,
            post,
        )

        content = request.data.get(
            "content",
            post.content,
        )

        visibility = request.data.get(
            "visibility",
            post.visibility,
        )

        post = update_post(
            post,
            content,
            visibility,
        )

        serializer = PostSerializer(
            post,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# ==========================================================
# DELETE POST
# ==========================================================

class DeletePostView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPostOwner,
    ]

    def delete(self, request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id,
        )

        self.check_object_permissions(
            request,
            post,
        )

        delete_post(post)

        return Response(
            {
                "message": "Post deleted successfully."
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# PIN POST
# ==========================================================

class PinPostView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPostOwner,
    ]

    def post(self, request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id,
        )

        self.check_object_permissions(
            request,
            post,
        )

        pin_post(post)

        return Response(
            {
                "message": "Post pinned successfully."
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# UNPIN POST
# ==========================================================

class UnpinPostView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPostOwner,
    ]

    def post(self, request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id,
        )

        self.check_object_permissions(
            request,
            post,
        )

        unpin_post(post)

        return Response(
            {
                "message": "Post unpinned successfully."
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# ARCHIVE POST
# ==========================================================

class ArchivePostView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPostOwner,
    ]

    def post(self, request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id,
        )

        self.check_object_permissions(
            request,
            post,
        )

        archive_post(post)

        return Response(
            {
                "message": "Post archived successfully."
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# RESTORE POST
# ==========================================================

class RestorePostView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsPostOwner,
    ]

    def post(self, request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id,
        )

        self.check_object_permissions(
            request,
            post,
        )

        restore_post(post)

        return Response(
            {
                "message": "Post restored successfully."
            },
            status=status.HTTP_200_OK,
        )