# Generated by Django 3.2 on 2023-12-04 10:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20231204_1235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ('name',), 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ('-pub_date',), 'verbose_name_plural': 'Тексты комментариев'},
        ),
        migrations.AlterModelOptions(
            name='genres',
            options={'ordering': ('name',), 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-pub_date',), 'verbose_name_plural': 'Тексты отзывов'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('name',), 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(help_text='Введите название катерогии', max_length=256, verbose_name='Название катерогии'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='slug',
            field=models.SlugField(help_text='Введите короткое название котеории', unique=True, verbose_name='Короткое название котеории'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='text',
            field=models.TextField(help_text='Введите текст комментария', verbose_name='Текст комментария'),
        ),
        migrations.AlterField(
            model_name='genres',
            name='name',
            field=models.CharField(help_text='Введите название жанров', max_length=256, verbose_name='Название жанра'),
        ),
        migrations.AlterField(
            model_name='genres',
            name='slug',
            field=models.SlugField(help_text='Введите короткое название жанров', unique=True, verbose_name='Короткое название жанров'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveIntegerField(help_text='Введите оценку произведения', validators=[django.core.validators.MinValueValidator(1, message='Оценка должна быть > 0!'), django.core.validators.MaxValueValidator(10, message='Оценка должна быть < 10!')], verbose_name='Оценка произведения'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(help_text='Введите текст отзыва', verbose_name='Текст отзыва'),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Выберите категория произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='reviews.categories', verbose_name='Категория произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, help_text='Введите описание произведения', null=True, verbose_name='Описание произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, help_text='Выберите жанр произведения', related_name='genre', to='reviews.Genres', verbose_name='Жанр произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(help_text='Введите название произведения', max_length=256, verbose_name='Введите название произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(help_text='Введите год выпуска произведения', verbose_name='Год выпуска произведения'),
        ),
    ]