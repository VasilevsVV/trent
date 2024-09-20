from typing import Any, Callable, Iterable, Optional, Tuple, TypeVar, overload

from trent.coll import icoll
from trent.concur import CPU_COUNT


T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')


@overload
def coll() -> icoll[Any]:...
@overload
def coll(seq: Iterable[Tuple[T1, T2]]) -> icoll[Tuple[T1, T2]]: ...
@overload
def coll(seq: Iterable[T]) -> icoll[T]: ...

def coll(seq: Optional[Iterable[T]] = None) -> icoll[T]:
    return icoll(seq)


def cmap(seq: Optional[Iterable[T]], f: Callable[[T], T2]) -> icoll[T2]:
    return icoll(seq).map(f)


def cfilter(seq: Optional[Iterable[T]], pred: Callable[[T], Any]) -> icoll[T]:
    return icoll(seq).filter(pred)


def pmap(seq: Optional[Iterable[T]], f: Callable[[T], T2]) -> icoll[T2]:
    return icoll(seq).pmap(f)


def pmap_(seq: Optional[Iterable[T]], f: Callable[[T], T2], threads: int = CPU_COUNT) -> icoll[T2]:
    return icoll(seq).pmap(f)


def cat(seq: Optional[Iterable[Iterable[T]]]) -> icoll[T]:
    return icoll(seq).cat()


def mapcat(seq: Optional[Iterable[T]], f: Callable[[T], Iterable[T2]]) -> icoll[T2]:
    return icoll(seq).mapcat(f)


def catmap(seq: Optional[Iterable[Iterable[T]]], f: Callable[[Any], T2]) -> icoll[T2]:
    return icoll(seq).catmap(f)


def pairmap(seq: Iterable[Tuple[T1, T2]], f:Callable[[T1, T2], T]) -> icoll[T]:
    return icoll(seq).pairmap(f)



@overload
def groupmap(seq: Iterable[Tuple[T1, Iterable[T2]]]) -> icoll[Tuple[T1, T2]]: ...
@overload
def groupmap(seq: Iterable[Tuple[T1, Iterable[T2]]], f:Callable[[T1, T2], T]) -> icoll[T]: ...

def groupmap(seq:Iterable[Tuple[T1, Iterable[T2]]], f:Optional[Callable[[T1, T2], T]] = None) -> icoll[T] | icoll[Tuple[T1, T2]]:
    if f is not None:
        return icoll(seq).groupmap(f)
    return icoll(seq).groupmap()



@overload
def map_to_pair(seq: Iterable[T], f_key:Callable[[T], T1]) -> icoll[Tuple[T1, T]]: ...
@overload
def map_to_pair(seq: Iterable[T], f_key:Callable[[T], T1], f_val: Callable[[T], T2]) -> icoll[Tuple[T1, T2]]: ...

def map_to_pair(seq: Iterable[T], f_key:Callable[[T], T1], f_val: Optional[Callable[[T], T2]] = None) -> icoll[Tuple[T1, T2]] | icoll[Tuple[T1, T]]:
    if f_val is not None:
        return icoll(seq).map_to_pair(f_key, f_val)
    return icoll(seq).map_to_pair(f_key)


if __name__ == '__main__':
    pass