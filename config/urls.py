from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    # =========================
    # AUTH
    # =========================

    path(
        "api/auth/",
        include("apps.accounts.urls"),
    ),

    # =========================
    # PROFILES
    # =========================

    path(
        "api/profiles/",
        include("apps.profiles.urls"),
    ),

    # =========================
    # POSTS
    # =========================

    path(
        "api/posts/",
        include("apps.posts.urls"),
    ),

    # =========================
    # FOLLOWERS
    # =========================

    path(
        "api/followers/",
        include("apps.followers.urls"),
    ),

    # =========================
    # NOTIFICATIONS
    # =========================

    path(
        "api/notifications/",
        include("apps.notifications.urls"),
    ),

    # =========================
    # MESSAGING
    # =========================

    path(
        "api/messaging/",
        include("apps.messaging.urls"),
    ),

    # =========================
    # SEARCH
    # =========================

    path(
        "api/search/",
        include("apps.search.urls"),
    ),

    # =========================
    # MODERATION
    # =========================

    path(
        "api/moderation/",
        include("apps.moderation.urls"),
    ),
]


# =========================
# MEDIA FILES
# =========================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )