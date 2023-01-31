"""IsAuthenticated permission class."""
from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in  ['TUTOR', 'ADMIN'])