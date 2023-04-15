from rest_framework import permissions


class IsAdmin(permissions.BasePermissions):
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
    