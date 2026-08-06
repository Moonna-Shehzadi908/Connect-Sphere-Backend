from django.shortcuts import get_object_or_404

from apps.posts.models import Post

from .models import Comment


def create_comment(
    *,
    author,
    post_id,
    content,
    parent_id=None,
):
    """
    Create a new comment or reply.
    """

    post = get_object_or_404(
        Post,
        id=post_id,
    )

    parent = None

    if parent_id:

        parent = get_object_or_404(
            Comment,
            id=parent_id,
        )

        # Prevent replies across different posts
        if parent.post != post:
            raise ValueError(
                "Parent comment belongs to another post."
            )

    comment = Comment.objects.create(
        author=author,
        post=post,
        parent=parent,
        content=content,
    )

    return comment