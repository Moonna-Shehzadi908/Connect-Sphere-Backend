from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from .models import Post, PostImage

User = get_user_model()


def get_timeline():
    return (
        Post.objects
        .select_related("author")
        .prefetch_related(
            Prefetch("images", queryset=PostImage.objects.all()),
            "hashtags",
            "mentions",
        )
        .filter(
            is_archived=False,
            visibility=Post.Visibility.PUBLIC,
        )
        .order_by("-created_at")
    )


def get_post(post_id):
    return (
        Post.objects
        .select_related("author")
        .prefetch_related(
            "images",
            "hashtags",
            "mentions",
        )
        .get(id=post_id)
    )


def get_user_posts(username):

    return (
        Post.objects
        .select_related("author")
        .prefetch_related(
            "images",
            "hashtags",
        )
        .filter(
            author__username=username,
            is_archived=False,
        )
        .order_by("-created_at")
    )