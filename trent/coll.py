from __future__ import annotations
from functools import reduce
from itertools import chain
from pprint import pprint
from typing import Callable, Iterable, Iterator, Optional, TypeVar, overload

T = TypeVar('T')
T1 = TypeVar('T1')
S = TypeVar('S')


class NestedIterationExceprion(Exception):
    def __repr__(self) -> str:
        return 'Nested iteration over `coll` class is invalid !!!'



class coll(Iterable[T]):
    def __init__(self, collection: Optional[Iterable[T]] = None) -> None:
        self.__coll: Iterable[T]
        self.__buffer: list[T]
        self.__iter: Iterator[T]
        self.__is_iterated: bool = False
        if collection is not None:
            self.__coll = collection
        else:
            self.__coll = []
    
    @property
    def collection(self) -> Iterable[T]:
        return self.__coll
    
    def map(self, f: Callable[[T], T1]) -> coll[T1]:
        return coll(map(f, self.__coll))
    
    
    def mapcat(self, f: Callable[[T], Iterable[T1]]) -> coll[T1]:
        m = map(f, self.__coll)
        m = reduce(chain, m)
        return coll(m)
    
    
    @overload
    def reduce(self, f: Callable[[S, T], S]) -> S|T: ...
    
    @overload
    def reduce(self, f: Callable[[S, T], S], initial: S) -> S: ...
    
    def reduce(self, f: Callable[[S, T], S], initial: Optional[S] = None) -> S | T:
        if initial is None:
            return reduce(f, self)
        return reduce(f, self, initial)
    
    
    def __iter__(self):
        if self.__is_iterated:
            raise NestedIterationExceprion
        self.__buffer = []
        self.__iter = iter(self.__coll)
        self.__is_iterated = True
        return self
    
    
    def __next__(self) -> T:
        try:
            val = next(self.__iter)
        except StopIteration:
            self.__coll = self.__buffer
            raise StopIteration
        self.__buffer.append(val)
        return val
    
    def __repr__(self) -> str:
        lst = list(self)
        return f'coll({lst})'





if __name__ == '__main__':
    def s_add(s1: str, s2: str):
        return s1 + s2
    c = coll([1,2,3,4]).map(lambda x: x+1).mapcat(lambda x: range(x)).map(str).reduce(s_add)
    pprint(c)