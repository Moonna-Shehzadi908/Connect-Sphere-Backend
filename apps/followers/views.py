from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FollowUserSerializer, UserFollowerSerializer
from .services import follow_user, get_followers, get_following, get_friend_suggestions, get_profile_stats


class FollowUserView(APIView):
    """
    Follow another user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, username):

        result = follow_user(
            follower=request.user,
            username=username,
        )

        if not result["success"]:
            return Response(
                {
                    "message": result["message"]
                },
                status=result["status"],
            )

        serializer = FollowUserSerializer(result["follow"])

        return Response(
            {
                "message": "User followed successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

from .services import follow_user, unfollow_user

class UnfollowUserView(APIView):
    """
    Unfollow another user.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, username):

        result = unfollow_user(
            follower=request.user,
            username=username,
        )

        if not result["success"]:
            return Response(
                {
                    "message": result["message"]
                },
                status=result["status"],
            )

        return Response(
            {
                "message": result["message"]
            },
            status=status.HTTP_200_OK,
        )
class FollowersListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):

        result = get_followers(username)

        if not result["success"]:
            return Response(
                {"message": result["message"]},
                status=result["status"],
            )

        serializer = UserFollowerSerializer(
            result["followers"],
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
class FollowingListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):

        result = get_following(username)

        if not result["success"]:
            return Response(
                {"message": result["message"]},
                status=result["status"],
            )

        serializer = UserFollowerSerializer(
            result["following"],
            many=True,
        )

        return Response(serializer.data)

class ProfileStatsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):

        result = get_profile_stats(username)

        if not result["success"]:
            return Response(
                {"message": result["message"]},
                status=result["status"],
            )

        return Response(result["stats"])

class FriendSuggestionsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = get_friend_suggestions(request.user)

        serializer = UserFollowerSerializer(
            users,
            many=True,
        )

        return Response(serializer.data)