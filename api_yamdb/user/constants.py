from enum import Enum


class MAX_LENGTH(Enum):
    ROLE: int = 20
    USERNAME: int = 150
    FIRST_NAME: int = 150
    LAST_NAME: int = 150
    EMAIL: int = 254
    CONFIRMATION_CODE: int = 255


class USER_MAX_LENGTH(Enum):
    USER_NAMES_LENGTH = 150
    USER_EMAIL_LENGTH = 254
