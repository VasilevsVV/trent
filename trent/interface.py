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


def cmap( f: Callable[[T], T2], seq: Optional[Iterable[T]]) -> icoll[T2]:
    return icoll(seq).map(f)


def cfilter(pred: Callable[[T], Any], seq: Optional[Iterable[T]]) -> icoll[T]:
    return icoll(seq).filter(pred)


def pmap(f: Callable[[T], T2], seq: Optional[Iterable[T]]) -> icoll[T2]:
    return icoll(seq).pmap(f)


def pmap_(f: Callable[[T], T2], seq: Optional[Iterable[T]], threads: int = CPU_COUNT) -> icoll[T2]:
    return icoll(seq).pmap(f)


def cat(seq: Optional[Iterable[Iterable[T]]]) -> icoll[T]:
    return icoll(seq).cat()


def mapcat(f: Callable[[T], Iterable[T2]], seq: Optional[Iterable[T]]) -> icoll[T2]:
    return icoll(seq).mapcat(f)


def catmap(f: Callable[[Any], T2], seq: Optional[Iterable[Iterable[T]]]) -> icoll[T2]:
    return icoll(seq).catmap(f)


def pairmap(f:Callable[[T1, T2], T], seq: Iterable[Tuple[T1, T2]], ) -> icoll[T]:
    return icoll(seq).pairmap(f)


def groupcoll(seq:Iterable[Tuple[T1, Iterable[T2]]]) -> icoll[Tuple[T1, T2]]:
    return icoll(seq).groupmap()


def groupmap(f:Callable[[T1, T2], T], seq:Iterable[Tuple[T1, Iterable[T2]]]) -> icoll[T] | icoll[Tuple[T1, T2]]:
    return icoll(seq).groupmap(f)


@overload
def map_to_pair(seq: Iterable[T], f_key:Callable[[T], T1]) -> icoll[Tuple[T1, T]]: ...
@overload
def map_to_pair(seq: Iterable[T], f_key:Callable[[T], T1], f_val: Callable[[T], T2]) -> icoll[Tuple[T1, T2]]: ...

def map_to_pair(seq: Iterable[T], f_key:Callable[[T], T1], f_val: Optional[Callable[[T], T2]] = None) -> icoll[Tuple[T1, T2]] | icoll[Tuple[T1, T]]:
    if f_val is not None:
        return icoll(seq).map_to_pair(f_key, f_val)
    return icoll(seq).map_to_pair(f_key)



def rangify(seq: Iterable[T]) -> icoll[Tuple[T, T]]:
    return icoll(seq).rangify()


if __name__ == '__main__':
    pass