from __future__ import annotations

import concurrent.futures as conc
from functools import reduce, cache
from funcy import filter
from itertools import chain
from pprint import pprint
from time import sleep
from typing import Any, Callable, Iterable, Iterator, Optional, TypeVar, overload

T = TypeVar('T')
T1 = TypeVar('T1')
S = TypeVar('S')


def __cpu_count():
    try:
        import psutil
        return psutil.cpu_count()
    except (ImportError, NotImplementedError):
        pass
    
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass
    return 8


DEFAULT_THREAD_COUNT = __cpu_count()


def __make_threadpool(threads: int = DEFAULT_THREAD_COUNT):
    return conc.ThreadPoolExecutor(threads)


TRENT_THREADPOOL = conc.ThreadPoolExecutor(DEFAULT_THREAD_COUNT, 'trent')
    



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
    
    
    # ==================================================================
    #           MAPS
    
    def map(self, f: Callable[[T], T1]) -> coll[T1]:
        return coll(map(f, self.__coll))
    
    
    def pmap(self, f: Callable[[T], S]) -> coll[S]:
        __map = TRENT_THREADPOOL.map(f, self.__coll)
        return coll(__map)
    
    
    def pmap_(self, f, threads=DEFAULT_THREAD_COUNT):
        assert threads >= 1, 'Async Thread count CAN NOT be < 1'
        if threads == 1:
            return self.map(f)
        with conc.ThreadPoolExecutor(threads) as p:
            __map = p.map(f, self.__coll)
        return coll(__map)
    
    
    def mapcat(self, f: Callable[[T], Iterable[T1]]) -> coll[T1]:
        m = map(f, self.__coll)
        m = reduce(chain, m)
        return coll(m)
    
    
    # ==================================================================
    #           TRANSFORMATIONS
    
    def concat(self, *__iterables: Iterable[T]) -> coll[T]:
        res = coll(self.__coll)
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
            return self
        self.__coll = chain(self.__coll, __iterable)
        return self
    
    def append_(self, __val: T) -> coll[T]:
        self.extend_([__val])
        return self
    
    
    # =================================================================
    #           COLLECTING
    
    @overload
    def reduce(self, f: Callable[[T, T], T]) -> T: ...
    
    @overload
    def reduce(self, f: Callable[[S, T], S], initial: S) -> S: ...
    
    def reduce(self, f: Callable, initial: Optional[S] = None) -> S | T:
        if initial is None:
            return reduce(f, self)
        return reduce(f, self, initial)
    
    
    def __iter__(self):
        if self.__is_iterated:
            raise NestedIterationExceprion
        self.__iter = iter(self.__coll)
        self.__is_iterated = True
        return self
    
    
    def __next__(self) -> T:
        try:
            return next(self.__iter)
        except StopIteration:
            self.__is_iterated = False
            raise StopIteration
    
    def __repr__(self) -> str:
        lst = list(self)
        return f'coll({lst})'



class pcoll(coll, Iterable[T]):
    def __init__(self, collection: Optional[Iterable[T]] = None) -> None:
        self.__buffer: list[T]
        super().__init__(collection)
    
    
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
            self.__is_iterated = False
            raise StopIteration
        self.__buffer.append(val)
        return val


if __name__ == '__main__':
    pass