from __future__ import annotations

import concurrent.futures as conc
from functools import reduce, cache
from funcy import filter, complement, take
from itertools import chain
from pprint import pprint
from time import sleep
from typing import Any, Callable, Dict, Generic, Hashable, Iterable, Iterator, Optional, Tuple, TypeVar, overload
from itertools import takewhile

from trent.concur import DEFAULT_THREAD_COUNT, TRENT_THREADPOOL
from trent.func import first, first_, identity, second, second_

T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
S = TypeVar('S')


class NestedIterationExceprion(Exception):
    def __repr__(self) -> str:
        return 'Nested iteration over `coll` class is invalid !!!'


class DistinctFilter(Generic[T]):
    def __init__(self, f:Callable[[T], Hashable]) -> None:
        self.__encounters = set()
        self.__f = f
    
    
    def __call__(self, val: T) -> bool:
        __val = self.__f(val)
        if __val in self.__encounters:
            return False
        self.__encounters.add(__val)
        return True


class icoll(Iterable[T]):
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
    
    # =================================================================
    #           TODO
    
    def _init_collection(self, collection:Optional[Iterable[T]]=None) -> Iterable[T]:
        if collection is None:
            return []
        elif isinstance(collection, icoll):
            return collection.collection
        elif isinstance(collection, Iterable):
            return collection
        else:
            raise Exception(f'Invalid collection type: {type(collection)}. Expected Iterable!')
    
    
    def __step(self, __coll: Iterable[S]) -> icoll[S]:
        return icoll(__coll)
    
    
    
    
    
    
    # def groupmap(self, f:Optional[Callable[[Any, Any], Any]]=None):
    #     pairs = self.mapcat(_unpack_group)
    #     if f:
    #         return pairs.pairmap(f)
    #     return pairs
    
    # def grouppmap(self, f:Callable[[Any, Any], Any]):
    #     pairs = self.mapcat(_unpack_group)
    #     return pairs.pairpmap(f)
    
    # def map_to_pair(self, f_key, f_val=_no_value()):
    #     f_val = _identity if isinstance(f_val, _no_value) else f_val
    #     return self.map(_make_pair_fn(f_key, f_val))
    
    # def pairmap(self, f:Callable[[Any, Any], Any]):
    #     return self.map(lambda p: f(first(p), second(p)))
    
    # def pairpmap(self, f:Callable[[Any, Any], Any]):
    #     return self.pmap(lambda p: f(first(p), second(p)))
    
    # def cat(self):
    #     return self.mapcat(_identity)
    
    # def rangify(self):
    #     self.collect()
    #     self._collection = zip(self._collection, list(self._collection)[1:])
    #     return self
    
    
    # def apply(self, f:Callable[[Any], Optional[Any]]):
    #     def __apply(el: Any):
    #         f(el)
    #         return el
    #     return self.map(__apply)
    
    
    # ==================================================================
    #           MAPS
    
    def map(self, f: Callable[[T], S]) -> icoll[S]:
        return self.__step(map(f, self.__coll))
    
    
    def pmap(self, f: Callable[[T], S]) -> icoll[S]:
        __map = TRENT_THREADPOOL.map(f, self.__coll)
        return self.__step(__map)
    
    
    def pmap_(self, f: Callable[[T], S], threads=DEFAULT_THREAD_COUNT) -> icoll[S]:
        assert threads >= 1, 'Async Thread count CAN NOT be < 1'
        if threads == 1:
            return self.map(f)
        with conc.ThreadPoolExecutor(threads) as p:
            __map = p.map(f, self.__coll)
        return self.__step(__map)
    
    
    def mapcat(self, f: Callable[[T], Iterable[T1]]) -> icoll[T1]:
        m = map(f, self.__coll)
        m = reduce(chain, m)
        return self.__step(m)
    
    
    def catmap(self, f: Callable[[Any], T1]) -> icoll[T1]:
        return self.mapcat(identity).map(f) # type: ignore
    
    
    def filter(self, f: Callable[[T], Any]) -> icoll[T]:
        return self.__step(filter(f, self.__coll))
    
    
    def remove(self, f: Callable[[T], Any]) -> icoll[T]:
        _f = complement(f)
        return self.filter(_f)
    
    
    def unique(self) -> icoll[T]:
        return self.distinct_by(identity)
    
    
    def distinct_by(self, f:Callable[[Any], Hashable]=identity) -> icoll[T]:
        __pred = DistinctFilter(f)
        return self.filter(__pred)
    
    
    def take(self, n: int)-> icoll[T]:
        assert n >= 0, 'You can only `take` >= 0 elements!'
        return self.__step(take(n, self.__coll))
    
    def takewhile(self, predicate:Callable[[T], bool]) -> icoll[T]:
        return self.__step(takewhile(predicate, self.__coll))
    
    
    # ==================================================================
    #           PAIRED
    
    def pairmap(self, f:Callable[[Any, Any], T1]) -> icoll[T1]:
        return self.map(lambda p: f(first(p), second(p)))
    
    
    def group_by_to_dict(self, f:Callable[[T], T1], val_fn: Callable[[T], T2] = identity) -> Dict[T1, list[T2]]:
        def __group(val: T) -> Tuple[T1, T2]:
            return (f(val), val_fn(val))
        pairs = self.map(__group).to_list()
        res: dict[T1, list[T2]] = {}
        for p in pairs:
            k,v = p
            if k in res:
                res[k].append(v)
            else:
                res[k] = [v]
        return res
    
    
    def group_by(self, f:Callable[[T], T1], val_fn: Callable[[T], T2] = identity) -> icoll[tuple[T1, list[T2]]]:
        d = self.group_by_to_dict(f, val_fn)
        return self.__step(d.items())
    
    
    # ==================================================================
    #           TRANSFORMATIONS
    
    def concat(self, *__iterables: Iterable[T]) -> icoll[T]:
        res = self.__step(self.__coll)
        for __it in __iterables:
            res.extend_(__it)
        return res
    
    def extend(self, __iterable: Iterable[T]) -> icoll[T]:
        return self.concat(__iterable)
    
    
    def conj(self, *vals: T):
        return self.concat(vals)
    
    
    def append(self, __val: T) -> icoll[T]:
        return self.__step(self.__coll).append_(__val)
    
    
    def cons(self, __val: T):
        return self.__step(chain([__val], self.__coll))

    
    def __add__(self, __iter: Iterable[T]) -> icoll[T]:
        return self.concat(__iter)
    
    # ===============================================================
    #   IN_PLACE TRANSFORMATIONS
    
    def extend_(self, __iterable: Iterable[T]) -> icoll[T]:
        """In-place extend. Addes `__iterable` to the end of `coll`.

        Args:
            __iterable (Iterable[T]): Iterable to be concatenated to the end

        Returns:
            coll[T]: Self
        """        
        if isinstance(__iterable, icoll):
            self.__coll = chain(self.__coll, __iterable.collection)
            return self
        self.__coll = chain(self.__coll, __iterable)
        return self
    
    def append_(self, __val: T) -> icoll[T]:
        self.extend_([__val])
        return self
    
    
    def cons_(self, __val: T):
        self.__coll = chain([__val], self.__coll)
    
    
    # =================================================================
    #           COLLECTING
    
    def to_list(self) -> list[T]:
        return list(self.__coll)
    
    
    def collect(self, f: Callable[[list[T]], S] = identity) -> S:
        return f(self.to_list())
    
    
    
    @overload
    def reduce(self, f: Callable[[T, T], T]) -> T: ...
    @overload
    def reduce(self, f: Callable[[S, T], S], initial: S) -> S: ...
    
    def reduce(self, f: Callable, initial: Optional[S] = None) -> S | T:
        if initial is None:
            return reduce(f, self)
        return reduce(f, self, initial)
    
    
    
    # ================================================================
    #           ITERATION
    
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
        # Persisting collection values. For easier debugging.
        self.__coll = list(self.__coll)
        return f'coll({self.__coll})'
    
    
    # ===============================================================
    #               UTIL
    
    def __group_pair_fn(self, f: Callable[[T], T1], val_fn: Callable[[T], T2] = identity) -> Callable[[T], Tuple[T1, T2]]:
        return lambda val: (f(val), val_fn(val))


class paired_coll(icoll, Iterable[Tuple[T1, T2]]):
    def __init__(self, collection: Iterable[Tuple[T1, T2]] | Dict[T1, T2] | None = None) -> None:
        super().__init__(collection)
    
    
    def _init_collection(self, collection:Iterable[Tuple[T1, T2]]|Dict[T1, T2]|None = None) -> Iterable[Tuple[T1, T2]]:
        if collection is None:
            return []
        elif isinstance(collection, paired_coll):
            return collection.__coll
        elif isinstance(collection, Dict):
            return collection.items() # type: ignore
        elif isinstance(collection, Iterable):
            return collection
        else:
            raise Exception(f'Invalid collection type: {type(collection)}. Expected Iterable!')
    
    
    # def __step(self, __coll: Iterable[Tuple[T1, T2]]) -> paired_coll[T1, T2]:
    #     return paired_coll(__coll)

    
    def pairmap(self, f:Callable[[T1, T2], S]) -> icoll[S]:
        return self.map(lambda p: f(first_(p), second_(p)))






if __name__ == '__main__':
    # c = paired_coll({1: 10}.items())
    # print(c)
    print(dict([(1,10), (2, 20)]))
    pass