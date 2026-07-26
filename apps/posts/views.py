from rest_framework import status
from rest_framework.parsers import (
    JSONParser,
    FormParser,
    MultiPartParser,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
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

        serializer = PostSerializer(post)

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
            )
            .order_by("-created_at")
        )

        serializer = PostSerializer(
            posts,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )