from enum import Enum


class ExtendedStrEnum(str, Enum):
    """Adds list method which will list all values associated with children instances."""

    @classmethod
    def list(cls) -> list[str]:
        return list(map(lambda c: c.value, cls))
