from __future__ import annotations

import itertools as it
from functools import reduce
from itertools import chain
from pprint import pprint
from typing import Any, Callable, Iterable, Iterator, Optional, TypeVar, overload

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
    
    
    def concat(self, *__iterables: Iterable[T]) -> coll[T]:
        res = coll()
        for __it in __iterables:
            res.extend_(__it)
        return res
    
    def extend(self, __iterable: Iterable[T]) -> coll[T]:
        return self.concat(__iterable)
    
    
    def append(self, __val: T) -> coll[T]:
        return coll(self.__coll).append_(__val)

    
    def __add__(self, __iter: Iterable[T]) -> coll[T]:
        return self.concat(__iter)
    
    # ===============================================================
    #   IN_PLACE TRANSFORMATIONS
    
    def extend_(self, __iterable: Iterable[T]) -> coll[T]:
        """In-place extend. Addes `__iterable` to the end of `coll`.

        Args:
            __iterable (Iterable[T]): Iterable to be concatenated to the end

        Returns:
            coll[T]: Self
        """        
        if isinstance(__iterable, coll):
            self.__coll = chain(self.__coll, __iterable.collection)
        self.__coll = chain(self.__coll, __iterable)
        return self
    
    def append_(self, __val: T) -> coll[T]:
        self.extend_([__val])
        return self
    
    
    
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
    c = coll([1,2,3,4])
    c = c.concat(b'56')
    pprint(c)