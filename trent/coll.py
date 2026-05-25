from __future__ import annotations
from typing import TYPE_CHECKING

import concurrent.futures as conc
from functools import cache, reduce
from itertools import chain, groupby, takewhile
from multiprocessing import Pool
from pprint import pprint
from time import sleep
from typing import (
    Any,
    Callable,
    Dict,
    Hashable,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    overload,
)

from funcy import complement, filter, take

from trent.coll_aux import DistinctFilter, EmptyCollectionException, NestedIterationExceprion, PartByCounter, PartCounter, Rangifier
from trent.collection_base import C, S, T, T1, T2, _no_value, icoll_base
from trent.concur import CPU_COUNT, TRENT_THREADPOOL
from trent.func import identity, isnone
from trent.nth import MissingValueException, first, first_, second, second_


if TYPE_CHECKING:
    from paired_coll import paired_icoll



class icoll(icoll_base, Iterable[T]):
    @classmethod
    def _step(cls: type[C], __coll: Iterable[S]) -> "icoll[S]":
        return icoll(__coll)
    

    def map_to_pair(self, f_key: Callable[[T], T1], f_val: Callable[[T], T2] = identity) -> paired_icoll[T1, T2]:
        from trent.paired_coll import paired_icoll
        def __pair(val: T) -> Tuple[T1, T2]:
            return (f_key(val), f_val(val))
        return paired_icoll(self.map(__pair))




# class persistent_coll(icoll_base, Iterable[T]):
#     def __init__(self, collection: Iterable | None = None) -> None:
#         self.__buffer: list[T] = []
#         self.__is_iterated: bool = False
#         super().__init__(collection)
    
    
#     def _step(self, __coll: Iterable[S]) -> icoll_base[S]:
#         return persistent_coll(__coll)
    
    
#     def _iter(self):
#         if self.__is_iterated:
#             raise NestedIterationExceprion
#         self._iterator = iter(self._coll)
#         self.__buffer = []
#         self.__is_iterated = True
#         return self
    
#     def _next(self):
#         try:
#             res = next(self._iterator)
#         except StopIteration:
#             self._coll = self.__buffer
#             self.__is_iterated = False
#             raise StopIteration
#         self.__buffer.append(res)
#         return res