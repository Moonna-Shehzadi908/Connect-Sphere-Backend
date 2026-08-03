from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.parsers import (
    JSONParser,
    FormParser,
    MultiPartParser,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Post,
    PostLike,
    Comment,
)
from .serializers import (
    PostSerializer,
    CommentSerializer,
)
from .services import create_post


# ==========================
# CREATE POST
# ==========================

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


# ==========================
# FEED
# ==========================

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


# ==========================
# LIKE / UNLIKE
# ==========================

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


# ==========================
# DELETE POST
# ==========================

class DeletePostView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id,
            author=request.user,
        )

        post.delete()

        return Response(
            {
                "message": "Post deleted successfully."
            },
            status=status.HTTP_200_OK,
        )


# ==========================
# ADD COMMENT
# ==========================

class CommentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):

        post = get_object_or_404(
            Post,
            id=post_id,
        )

        serializer = CommentSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save(
            post=post,
            author=request.user,
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


# ==========================
# DELETE COMMENT
# ==========================

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