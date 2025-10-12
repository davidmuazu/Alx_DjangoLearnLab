from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow full access to object owner; others have read-only access.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write only if owner
        return getattr(obj, 'author', None) == request.user
