from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Categories(models.Model):
    """Модель Категорий"""
    name = models.CharField('Название катерогии', max_length=256,
                            help_text='Введите название катерогии')
    slug = models.SlugField('Короткое название котеории',
                            unique=True, max_length=50,
                            help_text='Введите короткое название котеории')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='categories',
        null=True, blank=True, verbose_name='Автор'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name_plural = 'Категории'


class Genres(models.Model):
    """Модель Жанров"""
    name = models.CharField('Название жанра', max_length=256,
                            help_text='Введите название жанров')
    slug = models.SlugField('Короткое название жанров', unique=True,
                            max_length=50,
                            help_text='Введите короткое название жанров')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='genres',
        null=True, blank=True, verbose_name='Автор'
    )

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ("name",)
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель Произведений"""
    name = models.CharField('Введите название произведения', max_length=256,
                            help_text='Введите название произведения')
    year = models.IntegerField('Год выпуска произведения',
                               help_text='Введите год выпуска произведения')
    description = models.TextField('Описание произведения', null=True,
                                   blank=True,
                                   help_text='Введите описание произведения')
    genre = models.ManyToManyField(
        Genres, related_name='genre', blank=True,
        verbose_name='Жанр произведения',
        help_text='Выберите жанр произведения')
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category',
        verbose_name='Категория произведения',
        help_text='Выберите категория произведения'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='titles',
        null=True, blank=True, verbose_name='Автор'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    """Модель Отзывов"""
    text = models.TextField('Текст отзыва',
                            help_text='Введите текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления отзыва', auto_now_add=True, db_index=True,
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произвдение к которому будет оставлен отзыв'
    )
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message='Оценка должна быть > 0!'),
                    MaxValueValidator(10, message='Оценка должна быть < 10!')],
        verbose_name='Оценка произведения',
        help_text='Введите оценку произведения'
    )

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ('title', 'author',)
        ordering = ("-pub_date",)
        verbose_name_plural = 'Тексты отзывов'


class Comments(models.Model):
    """Модель Комментариев"""
    text = models.TextField('Текст комментария',
                            help_text='Введите текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления комментария', auto_now_add=True, db_index=True,
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв к которому будет оставлен комментарий'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("-pub_date",)
        verbose_name_plural = 'Тексты комментариев'
