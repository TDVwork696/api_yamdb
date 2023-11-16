from django.db import models


class Categories(models.Model):
    """Модель Категорий"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        pass
        ordering = ("name",)


class Genres(models.Model):
    """Модель Жанров"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Titles(models.Model):
    """Модель Произведений"""
    name = models.CharField(max_length=256)
    year = models.IntegerField('Год')
    description = models.TextField(null=True, blank=True)
    genre = models.ForeignKey(
        Genres, on_delete=models.PROTECT, related_name='genre')
    categories = models.ManyToManyField(
        Categories, related_name='categories', null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
