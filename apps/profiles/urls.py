from django.urls import path

from .views import (
    MyProfileView,
    UpdateProfileView,
    UploadAvatarView,
    UploadCoverView,
)

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="my-profile"),

    path(
        "me/update/",
        UpdateProfileView.as_view(),
        name="update-profile",
    ),

    path(
        "me/avatar/",
        UploadAvatarView.as_view(),
        name="upload-avatar",
    ),

    path(
        "me/cover/",
        UploadCoverView.as_view(),
        name="upload-cover",
    ),
]