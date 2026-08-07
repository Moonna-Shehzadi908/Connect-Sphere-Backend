from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CommentSerializer
from .services import create_comment, delete_comment


class CreateCommentView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        try:
            comment = create_comment(
                author=request.user,
                post_id=request.data.get("post"),
                parent_id=request.data.get("parent"),
                content=request.data.get("content"),
            )

        except ValueError as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CommentSerializer(comment)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class DeleteCommentView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(
        self,
        request,
        comment_id,
    ):

        try:
            delete_comment(
                comment_id=comment_id,
                user=request.user,
            )

        except ValueError as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                "message": "Comment deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT,
        )