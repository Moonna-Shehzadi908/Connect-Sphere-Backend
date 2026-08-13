from .models import Notification


def get_user_notifications(user):
    return Notification.objects.filter(
        recipient=user
    ).select_related(
        "sender"
    )


def get_notification(notification_id, user):
    return Notification.objects.get(
        id=notification_id,
        recipient=user,
    )