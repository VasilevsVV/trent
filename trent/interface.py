from typing import Any, Callable, Dict, Iterable, Optional, Tuple, TypeVar, overload

from trent.coll import Collection
from trent.concur import CPU_COUNT
from trent.paired_coll import PairedCollection


T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')


@overload
def seq() -> Collection[Any]:...
@overload
def seq(seq: Dict[T1, T2]) -> Collection[Tuple[T1, T2]]: ...
@overload
def seq(seq: Iterable[Tuple[T1, T2]]) -> Collection[Tuple[T1, T2]]: ...
@overload
def seq(seq: Iterable[T]) -> Collection[T]: ...

def seq(seq: Optional[Iterable] = None):
    if isinstance(seq, Dict):
        return Collection(seq.items())
    return Collection(seq)


def paired_seq(seq: Optional[Iterable[Tuple[T1, T2]]| Dict[T1, T2]]) -> PairedCollection[T1, T2]:
    if isinstance(seq, Dict):
        return PairedCollection(seq.items()) # type: ignore
    return PairedCollection(seq)


coll = seq
icoll = seq


def cmap( f: Callable[[T], T2], seq: Optional[Iterable[T]]) -> Collection[T2]:
    return Collection(seq).map(f)


def cfilter(pred: Callable[[T], Any], seq: Optional[Iterable[T]]) -> Collection[T]:
    return Collection(seq).filter(pred)


def pmap(f: Callable[[T], T2], seq: Optional[Iterable[T]]) -> Collection[T2]:
    return Collection(seq).pmap(f)


def pmap_(f: Callable[[T], T2], seq: Optional[Iterable[T]], threads: int = CPU_COUNT) -> Collection[T2]:
    return Collection(seq).pmap_(f, threads)


def cat(seq: Optional[Iterable[Iterable[T]]]) -> Collection[T]:
    return Collection(seq).cat()


def mapcat(f: Callable[[T], Iterable[T2]], seq: Optional[Iterable[T]]) -> Collection[T2]:
    return Collection(seq).mapcat(f)


def catmap(f: Callable[[Any], T2], seq: Optional[Iterable[Iterable[T]]]) -> Collection[T2]:
    return Collection(seq).catmap(f)


def pairmap(f:Callable[[T1, T2], T], seq: Iterable[Tuple[T1, T2]], ) -> Collection[T]:
    return Collection(seq).pairmap(f)


def groupcoll(seq:Iterable[Tuple[T1, Iterable[T2]]]) -> Collection[Tuple[T1, T2]]:
    return Collection(seq).groupmap()


def groupmap(f:Callable[[T1, T2], T], seq:Iterable[Tuple[T1, Iterable[T2]]]) -> Collection[T] | Collection[Tuple[T1, T2]]:
    return Collection(seq).groupmap(f)


@overload
def map_to_pair(seq: Iterable[T], f_key:Callable[[T], T1]) -> PairedCollection[T1, T]: ...
@overload
def map_to_pair(seq: Iterable[T], f_key:Callable[[T], T1], f_val: Callable[[T], T2]) -> PairedCollection[T1, T2]: ...

def map_to_pair(seq: Iterable[T], f_key:Callable[[T], T1], f_val: Optional[Callable[[T], T2]] = None) -> PairedCollection[T1, T2] | PairedCollection[T1, T]:
    if f_val is not None:
        return Collection(seq).map_to_pair(f_key, f_val)
    return Collection(seq).map_to_pair(f_key)



def rangify(_seq: Iterable[T]) -> PairedCollection[T, T]:
    return seq(_seq).rangify()
