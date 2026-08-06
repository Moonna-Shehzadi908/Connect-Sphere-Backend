from rest_framework.permissions import BasePermission


class IsPostOwner(BasePermission):
    """
    Allows only the owner of a post to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user