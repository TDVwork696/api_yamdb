from django.shortcuts import get_object_or_404
from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField

from reviews.models import Categories, Genres, Titles, Reviews, Comments


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


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Titles"""
    genre = GenresSerializer()
    categories = CategoriesSerializer(many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'categories')
        model = Titles

    def validate_year(self, value):
        """Проверяем год произведения"""
        if value < 1970 or value > 2023:
            raise serializers.ValidationError(
                'Год должен быть не раньше 1970 и не позже 2023'
            )
        return value


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Reviews"""
    score = serializers.IntegerField(min_value=1, max_value=10)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Reviews
        fields = ('id', 'text', 'author', 'score', 'created')
        read_only_fields = ('pub_date',)

    def validate_resending(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = get_object_or_404(
            Titles,
            id=self.context['request'].parser_context['kwargs']['title_id']
        )
        if Reviews.objects.filter(
            author=self.context['request'].user,
            title=title
        ).exists():
            raise serializers.ValidationError('Отзыв уже оставлен')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comments"""

    class Meta:
        model = Comments
        fields = (('id', 'text', 'author', 'created'))
        read_only_fields = ('pub_date',)
