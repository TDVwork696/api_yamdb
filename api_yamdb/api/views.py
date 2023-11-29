from django.core.mail import EmailMessage
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters import rest_framework as filters

from api.generic import CreateListDeleteViewSet
from reviews.models import Categories, Genres, Title, Review, Comments
from api.permissions import (IsAdminOrStaff)
from api.serializers import (CategoriesSerializer, GenresSerializer,
                             TitlesSerializer, TokenSerializer,
                             NotAdminSerializer, SignUpSerializer,
                             UsersSerializer, ReviewsSerializer,
                             CommentsSerializer, TitlesWriteSerializer)

from .filters import FilterSlug
from reviews.models import Categories, Genres, Titles, Reviews, Comments

from api_yamdb.settings import PROJECT_EMAIL
from user.models import (CustomUser)

from .permissions import IsAuthorOrModeratorOrAdmin


class CategoriesViewSet(CreateListDeleteViewSet):
    """Класс работы с категориями"""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    #permission_classes = (IsAuthorOrModeratorOrAdmin,)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(CreateListDeleteViewSet):
    """Класс для отображения Жанров"""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    #permission_classes = (IsAuthorOrModeratorOrAdmin,)
    filterset_fields = ('slug',)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    """Класс для работы с Произведениями."""
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    #permission_classes = (IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_class = FilterSlug
    #filterset_fields = (
    #    'name',
    #    'year',
    #    'genre__slug',
    #    'category__slug'
    #)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitlesWriteSerializer
        return TitlesSerializer


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

        email = request.data.get('email')
        username = request.data.get('username')

        users_set = CustomUser.objects.filter(
            username=username,
            email=email
        )

        if len(users_set) == 0:
            serializer = SignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        else:
            user = users_set[0]
            serializer = SignUpSerializer(user)

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
    http_method_names = ['get', 'post', 'patch', 'delete']

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
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrModeratorOrAdmin,)

    def get_title_id(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title = self.get_title_id()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = self.get_title_id()
        return title.reviews.all()


class CommentsViewSet(CreateListDeleteViewSet):
    """Класс для работы с Комментариями"""
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrModeratorOrAdmin,)

    def get_reviews_id(self):
        return get_object_or_404(Review, pk=self.kwargs.get('reviews_id'))

    def perform_create(self, serializer):
        reviews = self.get_reviews_id()
        serializer.save(author=self.request.user, reviews=reviews)

    def get_queryset(self):
        reviews = self.get_reviews_id()
        return reviews.comments.all()
