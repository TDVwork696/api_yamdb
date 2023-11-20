from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


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


class Reviews(models.Model):
    """Модель Отзывов"""
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message='Оценка должна быть > 0!'),
                    MaxValueValidator(10, message='Оценка должна быть < 10!')]
    )

    def __str__(self):
        return '"{}" and "{}"to title "{}" by author "{}"'.format(self.score,
                                                                  self.text,
                                                                  self.title,
                                                                  self.author)

    class Meta:
        ordering = ("-created",)


class Comments(models.Model):
    """Модель Комментариев"""
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("-created",)
