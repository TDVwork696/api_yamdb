from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    """Класс для пердоставления доступа на чтение всем,
    а на изменение только автору"""

    def has_object_permission(self, request, view, obj):
        """Возвращаем True если метод на чтение
        или если запрос делает автор."""
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )
