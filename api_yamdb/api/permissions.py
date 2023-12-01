from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# для доступа к пользователям
class IsAdminOrStaff(permissions.BasePermission):
    """"""
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff


# это будет основной пермишн
class IsAuthorOrModeratorOrAdmin(IsAuthenticatedOrReadOnly):
    """Класс пермишен, позволяющий читать данные всем.
    Изменения доступны только автору, модератору или админу"""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
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


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
