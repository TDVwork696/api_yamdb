from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsAdminOrStaff(permissions.BasePermission):
    """Класс пермишен, позволяющий читать и изменять данные только админу"""
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff


class IsReadOnlyOrAuthorOrModeratorOrAdmin(IsAuthenticatedOrReadOnly):
    """Класс пермишен, позволяющий читать данные всем.
    Изменения доступны только автору, модератору или админу"""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class IsAuthenticatedOrAdminOrReadOnly(permissions.BasePermission):
    """Класс пермишен, позволяющий читать данные всем.
    Изменения доступны только админу"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser
            )
        )
