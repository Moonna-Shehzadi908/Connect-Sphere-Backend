from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .models import Follow

User = get_user_model()

def follow_user(follower, username):
    """
    Create a follow relationship.

    Parameters
    ----------
    follower : User
        The authenticated user.

    username : str
        Username of the user to follow.
    """

    try:
        following = User.objects.get(username=username)

    except User.DoesNotExist:
        return {
            "success": False,
            "message": "User does not exist.",
            "status": 404,
        }

    if follower == following:
        return {
            "success": False,
            "message": "You cannot follow yourself.",
            "status": 400,
        }

    try:

        follow = Follow.objects.create(
            follower=follower,
            following=following,
        )

    except IntegrityError:

        return {
            "success": False,
            "message": "You are already following this user.",
            "status": 400,
        }

    return {
        "success": True,
        "follow": follow,
        "status": 201,
    }

def unfollow_user(follower, username):
    """
    Remove a follow relationship.
    """

    try:
        following = User.objects.get(username=username)

    except User.DoesNotExist:
        return {
            "success": False,
            "message": "User does not exist.",
            "status": 404,
        }

    try:
        follow = Follow.objects.get(
            follower=follower,
            following=following,
        )

    except Follow.DoesNotExist:
        return {
            "success": False,
            "message": "You are not following this user.",
            "status": 400,
        }

    follow.delete()

    return {
        "success": True,
        "message": f"You have unfollowed {following.username}.",
        "status": 200,
    }

def get_followers(username):
    """
    Return all followers of a user.
    """

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return {
            "success": False,
            "message": "User does not exist.",
            "status": 404,
        }

    followers = User.objects.filter(
        following__following=user
    ).select_related("profile")

    return {
        "success": True,
        "followers": followers,
        "status": 200,
    }
def get_following(username):

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return {
            "success": False,
            "message": "User does not exist.",
            "status": 404,
        }

    following = User.objects.filter(
        followers__follower=user
    ).select_related("profile")

    return {
        "success": True,
        "following": following,
        "status": 200,
    }
def get_profile_stats(username):

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return {
            "success": False,
            "message": "User does not exist.",
            "status": 404,
        }

    return {
        "success": True,
        "stats": {
            "followers": Follow.objects.filter(
                following=user
            ).count(),

            "following": Follow.objects.filter(
                follower=user
            ).count(),
        },
        "status": 200,
    }

from django.db.models import Q
import random


def get_friend_suggestions(user):

    users = User.objects.exclude(
        id=user.id
    ).exclude(
        followers__follower=user
    )

    users = list(users)

    random.shuffle(users)

    return users[:10]