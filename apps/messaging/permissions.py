from rest_framework.permissions import BasePermission


class IsConversationParticipant(BasePermission):
    """
    Allow access only to conversation participants.
    """

    def has_object_permission(self, request, view, obj):

        return obj.participants.filter(
            id=request.user.id
        ).exists()