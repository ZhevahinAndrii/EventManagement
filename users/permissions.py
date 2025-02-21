from rest_framework import permissions

class IsAdminOrCurrentUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_anonymous

    def has_object_permission(self, request, view, obj):
        return not request.user.is_anonymous and (request.method in permissions.SAFE_METHODS or request.user == obj or request.user.is_superuser)