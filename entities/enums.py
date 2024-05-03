from enum import Enum


class BaseEnum(str, Enum):
    """
    Base class for enumeration types that automatically handle case-insensitive value matching.
    """

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.value.lower() == value:
                return member
        raise KeyError(f"No value found for '{value}' in {cls.__name__}")
