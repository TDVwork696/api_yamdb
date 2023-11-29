from datetime import datetime
import re

from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Categories, Genres, Title, Review, Comments
from user.models import CustomUser

from api_yamdb.settings import USER_NAMES_LENGTH, USER_EMAIL_LENGTH


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categories"""

    class Meta:
        fields = ('name', 'slug')
        model = Categories
        lookup_field = 'slug'
        lookup_value_regex = r"(^[-a-zA-Z0-9_]+$)"


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genres"""

    class Meta:
        fields = ('name', 'slug')
        model = Genres
        lookup_field = 'slug'
        lookup_value_regex = r"(^[-a-zA-Z0-9_]+$)"


class TitlesWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title"""
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        """Проверяем год произведения"""
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Год должен быть текущий или меньше'
            )
        return value


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title"""
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'confirmation_code'
        )


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=USER_NAMES_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    email = serializers.EmailField(
        max_length=USER_EMAIL_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                "Нельзя назвать пользователя 'me'."
            )
        if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', username) is None:
            raise serializers.ValidationError(
                f'Имя пользователя содержит недопустимые символы {username}.'
            )
        return username

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""
    score = serializers.IntegerField(min_value=1, max_value=10)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы не можете добавить более'
                    'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'created')
        read_only_fields = ('pub_date',)


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comments"""

    class Meta:
        model = Comments
        fields = (('id', 'text', 'author', 'created'))
        read_only_fields = ('pub_date',)
