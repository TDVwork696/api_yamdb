from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from django.core.exceptions import PermissionDenied

from reviews.models import Categories, Genres, Titles
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesSerializer)
from .generic import CreateListDeleteViewSet


class CategoriesViewSet(CreateListDeleteViewSet):
    """Класс работы с категориями"""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class GenresViewSet(CreateListDeleteViewSet):
    """Класс для отображения Жанров"""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    """Класс для работы с Произведениями."""
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination

    def perform_update(self, serializer):
        """Проверяем кто делает запросы PUT и PATCH.
        Если это не автор, то возвращаем ошибку что доступ только у автора """
        # пока вставил простую проверку на автора. Но нужно будет доработать.
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("Изменения доступны только ?")
        return super().perform_update(serializer)
