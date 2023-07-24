from rest_framework import permissions

class OnlyAuthorOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_authenticated:
            return True

        return request.method in permissions.SAFE_METHODS