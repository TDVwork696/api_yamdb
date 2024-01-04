import re
from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Categories, Genres, Title, Review, Comments
from user.constants import USER_MAX_LENGTH
from user.models import CustomUser


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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')
        model = Title


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Токена"""
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
    """Сериализатор для модели Пользователя"""
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
    """Сериализатор для модели NotAdmin"""
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
    """Сериализатор для модели SignUp"""
    username = serializers.CharField(
        max_length=USER_MAX_LENGTH.USER_NAMES_LENGTH.value,
        required=True
    )

    email = serializers.EmailField(
        max_length=USER_MAX_LENGTH.USER_EMAIL_LENGTH.value,
        required=True
    )

    def validate(self, data):
        username = data['username']
        email = data['email']

        if username == 'me':
            raise serializers.ValidationError(
                "Нельзя назвать пользователя 'me'."
            )
        if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', username) is None:
            raise serializers.ValidationError(
                f'Имя пользователя содержит недопустимые символы {username}.'
            )
        users_set = CustomUser.objects.filter(username=username)
        if len(users_set) != 0:
            if users_set[0].email != email:
                raise serializers.ValidationError(
                    f'Имя пользователя {username} занято.'
                )
            else:
                return data
        users_set = CustomUser.objects.filter(email=email)
        if len(users_set) != 0 and users_set[0].username != username:
                raise serializers.ValidationError(
                    f'Почта {email} уже используется.'
                )
        return data

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
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('pub_date',)


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comments"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('pub_date',)
