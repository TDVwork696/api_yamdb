from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField

from reviews.models import Categories, Genres, Titles


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
