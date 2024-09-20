from typing import Any, Iterable, Optional, Sequence, TypeVar


class MissingValueException(Exception):
    def __init__(self, val, fn_name: str) -> None:
        self._value = val
        self._fn_name = fn_name
    
    def __repr__(self) -> str:
        return f'Missing {self._fn_name} for value: {self._value}'


class __no_value():
    def __init__(self) -> None:
        pass

# ======================================================

_T = TypeVar('_T')
_T2 = TypeVar('_T2')


def identity(val: _T) -> _T:
    return val

# =======================================================


def _nth(coll:Optional[Iterable[_T]], n:int, position_name, default:_T2 = None) -> _T|_T2:
    if (isinstance(coll, Sequence)):
        if len(coll) > n:
            return coll[n]
        return default
    if isinstance(coll, Iterable):
        it = iter(coll)
        i = 0
        while i < n:
            try:
                next(it)
            except StopIteration:
                return default
            i += 1
        try:
            return next(it)
        except StopIteration:
            return default
    if coll is None:
        return default
    raise Exception("Cant get '{}' attribute from value: {}.\n It is not a Collection|None".format(position_name, coll))

def first(coll: Iterable[_T]|Any) -> Optional[_T]:
    return _nth(coll, 0, 'first')

def second(coll: Iterable[_T]|Any) -> Optional[_T]:
    return _nth(coll, 1, 'second')

def third(coll: Iterable[_T]|Any) -> Optional[_T]:
    return _nth(coll, 2, 'third')

def nth(coll: Iterable[_T]|Any, n:int) -> Optional[_T]:
    return _nth(coll, n, 'nth')


def first_(coll: Iterable[_T]) -> _T:
    res = _nth(coll, 0, 'first_', __no_value())
    if isinstance(res, __no_value):
        raise MissingValueException(coll, 'first')
    return res


def second_(coll: Iterable[_T]) -> _T:
    res = _nth(coll, 1, 'second_', __no_value())
    if isinstance(res, __no_value):
        raise MissingValueException(coll, 'second')
    return res


