from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination


from reviews.models import Categories, Genres, Titles, Reviews, Comments
from .generic import CreateListDeleteViewSet
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesSerializer, ReviewsSerializer,
                          CommentsSerializer)
from .permissions import OwnerOrReadOnly


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


class ReviewsViewSet(CreateListDeleteViewSet):
    """Класс для работы с Отзывами"""
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = OwnerOrReadOnly

    def get_title_id(self):
        return get_object_or_404(Titles, pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title = self.get_title_id()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = self.get_title_id()
        return title.comments.all()


class CommentsViewSet(CreateListDeleteViewSet):
    """Класс для работы с Комментариями"""
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = OwnerOrReadOnly

    def get_reviews_id(self):
        return get_object_or_404(Reviews, pk=self.kwargs.get('reviews_id'))

    def perform_create(self, serializer):
        reviews = self.get_reviews_id()
        serializer.save(author=self.request.user, reviews=reviews)

    def get_queryset(self):
        reviews = self.get_reviews_id()
        return reviews.comments.all()
