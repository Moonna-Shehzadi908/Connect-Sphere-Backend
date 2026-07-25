from django.contrib import admin

from .models import (
    Post,
    PostImage,
    Hashtag,
    Mention,
)


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "author",
        "visibility",
        "created_at",
    )

    list_filter = (
        "visibility",
        "created_at",
    )

    search_fields = (
        "author__username",
        "content",
    )

    inlines = [
        PostImageInline,
    ]


admin.site.register(Hashtag)
admin.site.register(Mention)