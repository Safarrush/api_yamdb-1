from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class AdminModeratorAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST' and request.user.is_authenticated:
            return True
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_moderator
            or request.user == obj.author)
