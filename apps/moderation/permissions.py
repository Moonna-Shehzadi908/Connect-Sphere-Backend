from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Allows access to moderators and admins.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role in [
                "moderator",
                "admin",
            ]
        )