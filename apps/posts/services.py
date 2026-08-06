import re

from django.contrib.auth import get_user_model

from .models import (
    Hashtag,
    Mention,
    Post,
    PostImage,
)

User = get_user_model()


def create_post(
    *,
    author,
    content,
    visibility,
    images,
):

    post = Post.objects.create(
        author=author,
        content=content,
        visibility=visibility,
    )

    for image in images:

        PostImage.objects.create(
            post=post,
            image=image,
        )

    hashtags = re.findall(
        r"#(\w+)",
        content,
    )

    for tag in hashtags:

        hashtag, created = Hashtag.objects.get_or_create(
            name=tag.lower()
        )

        hashtag.posts.add(post)

    mentions = re.findall(
        r"@(\w+)",
        content,
    )

    for username in mentions:

        try:

            user = User.objects.get(
                username=username
            )

            Mention.objects.create(
                post=post,
                user=user,
            )

        except User.DoesNotExist:
            continue

    return post

from django.shortcuts import get_object_or_404

from .models import Post


def update_post(post, content, visibility):
    """
    Update an existing post.
    """
    post.content = content
    post.visibility = visibility
    post.is_edited = True
    post.save()

    return post


def delete_post(post):
    """
    Delete a post.
    """
    post.delete()

from django.db import transaction


@transaction.atomic
def pin_post(post):
    """
    Pin a post and unpin any other posts
    owned by the same user.
    """

    Post.objects.filter(
        author=post.author,
        is_pinned=True,
    ).update(is_pinned=False)

    post.is_pinned = True
    post.save(update_fields=["is_pinned"])

    return post


def unpin_post(post):
    """
    Remove pinned status.
    """
    post.is_pinned = False
    post.save(update_fields=["is_pinned"])

    return post


def archive_post(post):
    """
    Archive a post.
    """
    post.is_archived = True
    post.save(update_fields=["is_archived"])

    return post


def restore_post(post):
    """
    Restore an archived post.
    """
    post.is_archived = False
    post.save(update_fields=["is_archived"])

    return post