from enum import Enum


class MaxLength(Enum):
    SLUG: int = 50
    NAME: int = 256


class Score(Enum):
    MIN_VALUE_VALIDATOR: int = 1
    MAX_VALUE_VALIDATOR: int = 10


class Categories(Enum):
    NAME: int = 50
    SLUG: int = 50


class Genres(Enum):
    NAME: int = 50
    SLUG: int = 50


class Title(Enum):
    NAME: int = 50
