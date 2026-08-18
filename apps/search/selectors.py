from django.contrib.auth import get_user_model
from django.db.models import Q
from apps.posts.models import Post
from django.db.models import Count
from apps.posts.models import Hashtag
from django.shortcuts import get_object_or_404

User = get_user_model()


def search_users(query):
    """
    Search users by username,
    first name or last name.
    """

    return (
        User.objects
        .filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        .order_by("username")
    )

def search_posts(query):
    """
    Search posts by content.
    """

    return (
        Post.objects
        .select_related("author")
        .filter(
            Q(content__icontains=query)
        )
        .order_by("-created_at")
    )



def search_hashtags(query):
    """
    Search hashtags by name.
    """

    return (
        Hashtag.objects
        .filter(
            name__icontains=query
        )
        .annotate(
            posts_count=Count("posts")
        )
        .order_by(
            "-posts_count",
            "name",
        )
    )




def get_posts_by_hashtag(name):
    """
    Return all posts belonging to a hashtag.
    """

    hashtag = get_object_or_404(
        Hashtag,
        name=name.lower(),
    )

    return (
        hashtag.posts
        .select_related("author")
        .prefetch_related("images")
        .order_by("-created_at")
    )


def get_trending_hashtags():
    """
    Return hashtags ordered by
    number of associated posts.
    """

    return (
        Hashtag.objects
        .annotate(
            posts_count=Count("posts")
        )
        .filter(
            posts_count__gt=0
        )
        .order_by(
            "-posts_count",
            "name",
        )
    )

def get_search_suggestions(query):

    users = (
        User.objects
        .filter(username__icontains=query)
        .order_by("username")[:5]
    )

    hashtags = (
        Hashtag.objects
        .filter(name__icontains=query)
        .order_by("name")[:5]
    )

    posts = (
        Post.objects
        .select_related("author")
        .filter(content__icontains=query)
        .order_by("-created_at")[:5]
    )

    return {
        "users": users,
        "hashtags": hashtags,
        "posts": posts,
    }
def global_search(query):

    return {
        "users": search_users(query)[:10],
        "posts": search_posts(query)[:10],
        "hashtags": search_hashtags(query)[:10],
    }