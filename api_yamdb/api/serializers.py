from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categories"""

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genres"""

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Titles"""
    genre = GenresSerializer(read_only=True)
    categories = CategoriesSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'categories')
        model = Titles
