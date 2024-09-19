from typing import Any, TypeVar



T = TypeVar('T')


def identity(val: T) -> T:
    return val 