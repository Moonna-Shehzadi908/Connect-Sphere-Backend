from rest_framework import status
from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostSerializer
from .services import create_post


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