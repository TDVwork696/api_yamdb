from enum import Enum


class MAX_LENGTH(Enum):
    SLUG = 50
    NAME = 256


class SCORE(Enum):
    MINVALUEVALIDATOR = 1
    MAXVALUEVALIDATOR = 10
