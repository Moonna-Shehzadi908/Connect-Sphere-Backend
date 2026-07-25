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