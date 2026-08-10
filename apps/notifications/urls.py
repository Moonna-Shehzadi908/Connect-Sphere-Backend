from django.urls import path

from .views import (
    NotificationListView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView,
    DeleteNotificationView,
    UnreadNotificationCountView,
)

urlpatterns = [

    path(
        "",
        NotificationListView.as_view(),
        name="notifications",
    ),

    path(
        "<int:notification_id>/read/",
        MarkNotificationReadView.as_view(),
        name="notification-read",
    ),

    path(
        "read-all/",
        MarkAllNotificationsReadView.as_view(),
        name="notifications-read-all",
    ),

    path(
        "<int:notification_id>/",
        DeleteNotificationView.as_view(),
        name="notification-delete",
    ),

    path(
        "unread-count/",
        UnreadNotificationCountView.as_view(),
        name="notification-unread-count",
    ),
]