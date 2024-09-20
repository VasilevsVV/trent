from typing import Any, Iterable, Optional, Sequence, TypeVar


class MissingValueException(Exception):
    def __init__(self, val, fn_name: str) -> None:
        self._value = val
        self._fn_name = fn_name
    
    def __repr__(self) -> str:
        return f'Missing {self._fn_name} for value: {self._value}'

# ======================================================

_T = TypeVar('_T')


def identity(val):
    return val


# def _unpack_group(group):
#     key, vals = group
#     return [(key, v) for v in vals]

# def _make_group_pair(f, val_fn: Callable[[Any], Any] = _identity):
#     return lambda val: (f(val), val_fn(val))

# def _make_pair_fn(f_key, f_val):
#     return lambda val: (f_key(val), f_val(val))


# =======================================================


def _nth(coll:Optional[Iterable[_T]], n:int, position_name) -> Optional[_T]:
    if (isinstance(coll, Sequence)):
        if len(coll) > n:
            return coll[n]
        return None
    if isinstance(coll, Iterable):
        it = iter(coll)
        i = 0
        while i < n:
            next(it)
            i += 1
        return next(it)
    if coll is None:
        return None
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
    res = _nth(coll, 0, 'first_')
    if res is None:
        raise MissingValueException(coll, 'first')
    return res


def second_(coll: Iterable[_T]) -> _T:
    res = _nth(coll, 1, 'second_')
    if res is None:
        raise MissingValueException(coll, 'second')
    return res