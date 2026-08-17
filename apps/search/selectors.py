from django.contrib.auth import get_user_model
from django.db.models import Q
from apps.posts.models import Post

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