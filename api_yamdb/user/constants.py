from enum import Enum


class User(Enum):
    USERNAME_LEN: int = 150
    EMAIL_LEN: int = 254
    ROLE_LEN: int = 20
    FIRST_NAME_LEN: int = 150
    LAST_NAME_LEN: int = 150
    CONFIRMATION_CODE_LEN: int = 255
