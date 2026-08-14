from django.contrib.auth import get_user_model
from django.db import IntegrityError
import random

from .models import Follow


User = get_user_model()


# ==========================================================
# FOLLOW USER
# ==========================================================

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
        following = User.objects.get(
            username=username
        )

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


# ==========================================================
# UNFOLLOW USER
# ==========================================================

def unfollow_user(follower, username):
    """
    Remove a follow relationship.
    """

    try:
        following = User.objects.get(
            username=username
        )

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


# ==========================================================
# GET FOLLOWERS
# ==========================================================

def get_followers(username):
    """
    Return all followers of a user.
    """

    try:
        user = User.objects.get(
            username=username
        )

    except User.DoesNotExist:

        return {
            "success": False,
            "message": "User does not exist.",
            "status": 404,
        }

    # Find Follow records where this user
    # is the person being followed.

    follows = Follow.objects.filter(
        following=user
    ).select_related(
        "follower",
        "follower__profile",
    )

    # Get the actual User objects
    # who follow this user.

    followers = [
        follow.follower
        for follow in follows
    ]

    return {
        "success": True,
        "followers": followers,
        "status": 200,
    }


# ==========================================================
# GET FOLLOWING
# ==========================================================

def get_following(username):
    """
    Return all users that this user is following.
    """

    try:
        user = User.objects.get(
            username=username
        )

    except User.DoesNotExist:

        return {
            "success": False,
            "message": "User does not exist.",
            "status": 404,
        }

    # Find Follow records where this user
    # is the person doing the following.

    follows = Follow.objects.filter(
        follower=user
    ).select_related(
        "following",
        "following__profile",
    )

    # Get the actual User objects
    # being followed.

    following = [
        follow.following
        for follow in follows
    ]

    return {
        "success": True,
        "following": following,
        "status": 200,
    }


# ==========================================================
# PROFILE FOLLOW STATS
# ==========================================================

def get_profile_stats(username):

    try:
        user = User.objects.get(
            username=username
        )

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


# ==========================================================
# FRIEND SUGGESTIONS
# ==========================================================

def get_friend_suggestions(user):

    users = User.objects.exclude(
        id=user.id
    ).exclude(
        followers__follower=user
    )

    users = list(users)

    random.shuffle(users)

    return users[:10]