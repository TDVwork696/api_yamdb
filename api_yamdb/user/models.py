from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.validators import validate_username
from .constants import Max_length

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE_LIST = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
]


class CustomUser(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        validators=(validate_username,),
        max_length=Max_length.max_length_150.value,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=Max_length.max_length_254.value,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=Max_length.max_length_20.value,
        choices=ROLE_LIST,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=Max_length.max_length_150.value,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=Max_length.max_length_150.value,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=Max_length.max_length_255.value,
        null=True,
        blank=False,
        default='None'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


@receiver(post_save, sender=CustomUser)
def post_save(sender, instance, created, **kwargs):
    """Для создаваемых пользователей заполняем код подтверждения."""
    if created:
        confirmation_code = default_token_generator.make_token(instance)
        instance.confirmation_code = confirmation_code
        instance.save()
