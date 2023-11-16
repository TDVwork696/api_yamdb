from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Categories, Genres, Titles
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesSerializer)


class CategoriesViewSet(viewsets.ModelViewSet):
    """Класс работы с категориями"""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination


class GenresViewSet(viewsets.ModelViewSet):
    """Класс для отображения Жанров"""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination


class TitlesViewSet(viewsets.ModelViewSet):
    """Класс для работы с Произведениями."""
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
