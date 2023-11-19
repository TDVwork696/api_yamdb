import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидация юзернэйма."""
    if value == 'me':
        raise ValidationError(
            ('Недопустимое имя пользователя - me.'),
            params={'value': value},
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Имя пользователя содержит недопустимые символы {value}.'),
            params={'value': value},
        )
