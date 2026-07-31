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
)
from .serializers import PostSerializer
from .services import create_post


class CreatePostView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

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


class PostListView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

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


class ToggleLikeView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

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