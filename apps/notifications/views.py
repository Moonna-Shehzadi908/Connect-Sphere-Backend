from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.core.pagination import DefaultPagination

from .selectors import get_user_notifications
from .serializers import NotificationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .selectors import (get_user_notifications,get_notification,)

from .services import (mark_notification_as_read,mark_all_notifications_as_read,)

class NotificationListView(ListAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = NotificationSerializer

    pagination_class = DefaultPagination

    def get_queryset(self):
        return get_user_notifications(
            self.request.user
        )

class MarkNotificationReadView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):

        notification = get_notification(
            notification_id,
            request.user,
        )

        mark_notification_as_read(notification)

        return Response(
            {
                "message": "Notification marked as read."
            },
            status=status.HTTP_200_OK,
        )

class MarkAllNotificationsReadView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        updated = mark_all_notifications_as_read(
            request.user
        )

        return Response(
            {
                "updated": updated
            },
            status=status.HTTP_200_OK,
        )

class DeleteNotificationView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, notification_id):

        notification = get_notification(
            notification_id,
            request.user,
        )

        notification.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class UnreadNotificationCountView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        count = request.user.notifications.filter(
            is_read=False
        ).count()

        return Response(
            {
                "unread_count": count
            }
        )