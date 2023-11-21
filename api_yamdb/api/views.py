from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.generic import CreateListDeleteViewSet
from reviews.models import Categories, Genres, Titles, Reviews, Comments
from api.permissions import (IsAdminOrStaff)
from api.serializers import (CategoriesSerializer, GenresSerializer,
                             TitlesSerializer, TokenSerializer,
                             NotAdminSerializer, SignUpSerializer,
                             UsersSerializer, ReviewsSerializer,
                             CommentsSerializer)
from api_yamdb.settings import PROJECT_EMAIL
from user.models import (CustomUser)



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


class APIGetToken(APIView):
    """Получение токена."""
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(CustomUser, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'confirmation_code': 'Неверный код!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class APISignup(APIView):
    """Отправка кода на email пользователя."""
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email=PROJECT_EMAIL,
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Добро пожаловать, {user.username}!'
            f'Доступ к API по коду: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код доступа'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """Вью-сет пользователя."""
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdminOrStaff,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            serializer = NotAdminSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
