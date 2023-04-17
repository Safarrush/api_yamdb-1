from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == 'admin' or request.user.is_superuser)
        return request.method in permissions.SAFE_METHODS
    

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    

class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'user'
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )
    

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return(
                request.user.role == 'admin' or request.user.is_superuser
            )
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return(
                request.user.role == 'admin' or request.user.is_superuser
            )
        return False
