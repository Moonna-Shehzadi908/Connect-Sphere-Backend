from .models import Notification


def create_notification(recipient,sender,notification_type,message,):
    """
    Create a notification unless the sender
    and recipient are the same user.
    """

    if recipient == sender:
        return None

    return Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        message=message,
    )

def mark_notification_as_read(notification):
    """
    Mark a single notification as read.
    """

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    return notification


def mark_all_notifications_as_read(user):
    """
    Mark every notification belonging to a user as read.
    """

    return Notification.objects.filter(
        recipient=user,
        is_read=False,
    ).update(is_read=True)