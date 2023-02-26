from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        if (request.method in SAFE_METHODS and request.user
           and request.is_authenticated):
            return (
                request.user.is_superuser
                or obj.author == request.user
            )
        return False
