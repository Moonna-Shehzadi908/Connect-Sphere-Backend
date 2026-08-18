import re

from .models import Hashtag

def extract_hashtags(content):
    """
    Extract hashtags from post content.
    """

    hashtags = re.findall(
        r"#(\w+)",
        content,
    )

    return list(
        {
            tag.lower()
            for tag in hashtags
        }
    )
def save_hashtags(post, hashtag_names):
    """
    Create missing hashtags and attach them to the post.
    """

    for name in hashtag_names:

        hashtag, _ = Hashtag.objects.get_or_create(
            name=name
        )

        hashtag.posts.add(post)