from __future__ import annotations
from typing import TYPE_CHECKING

from typing import Any, Callable, Dict, Generic, Iterable, TypeVar, Tuple, overload
from trent.coll_aux import Rangifier
from trent.exceptions import EmptyCollectionException
from trent.func import identity
from trent.nth import first, first_, second, second_
from trent.collection_core import C, R1, R2, T1, T2, Collection

if TYPE_CHECKING:
    from trent.coll import CollectionImpl


class PairedCollection(Collection[Tuple[T1, T2]], Iterable[Tuple[T1, T2]]):


    def pairmap(self, f:Callable[[T1, T2], R1]) -> Collection[R1]:
        """Map over paired elements (tuple, list, Iterable, etc.) with `f(arg1, arg2)` function.
        WARNING: sequence elements MUST be iterables.
        NOTE: Iterable elements can contain more than 2 elements, but extra values will be lost.
        NOTE: If elements contain less than 2 values - `None` will be passed to `f` instead.

        Args:
            f (Callable[[Any, Any], T1]): _description_

        Returns:
            icoll[T1]: _description_
        """
        def _f(_val: Tuple[T1, T2]):
            return f(first_(_val), second_(_val))
        return self._mapping_step(self).map(_f)
    

    def pairmap_to_pair(self, f: Callable[[T1, T2], Tuple[R1, R2]]) -> PairedCollection[R1, R2]:
        return PairedCollection(self.pairmap(f))
    

    def group_by(
            self, 
            f:Callable[[Tuple[T1, T2]], R1], 
            val_fn: Callable[[Tuple[T1, T2]], R2] = identity
            ) -> "PairedCollection[R1, list[R2]]":
        d = self.group_by_to_dict(f, val_fn)
        return PairedCollection(d.items())
    

    def map_to_pair(self, f_key: Callable[[Tuple[T1, T2]], R1], f_val: Callable[[Tuple[T1, T2]], R2] = identity) -> "PairedCollection[R1, R2]":
        def __pair(val: Tuple[T1, T2]) -> Tuple[R1, R2]:
            return (f_key(val), f_val(val))
        return PairedCollection(self.map(__pair))
    

    def to_dict(self) -> dict[T1, T2]:
        return dict(self)


    def __repr__(self) -> str:
        return f'paired_coll({self._coll})'
    

    def as_spans(self, *, fail_if_single: bool = False) -> PairedCollection[tuple[T1, T2], tuple[T1, T2]]:
        """
        Pairs all adjacent elements in the collection into overlapping pairs (spans).

        This method operates entirely lazily as a sliding window of size 2, 
        matching each element with its immediate successor.

        WARNING: If `fail_if_single` is not provided, and a collection only contains 1 element:
            only one span of the same element will be created: `seq([1]).as_spans() => seq([(1, 1)])`

        Returns:
            PairedCollection[Tuple[T, T]]: A new PairedCollection containing the adjacent tuples.
            fail_if_single (bool, optional): Indicates wether to fail if Collection only contains 1 elemnt. Defaults to False.

        Examples:
            >>> list(CollectionBase([1, 2, 3, 4]).as_spans())
            [(1, 2), (2, 3), (3, 4)]

            >>> list(CollectionBase([1]).as_spans())
            [(1, 1)]

            >>> list(CollectionBase(['A', 'B', 'C']).as_spans())
            [('A', 'B'), ('B', 'C')]
        """
        from trent.paired_coll import PairedCollection
        try:
            __init_val = self.head
        except EmptyCollectionException:
            return PairedCollection()
        _tail = self.tail()
        if _tail.empty:
            if fail_if_single:
                raise EmptyCollectionException("Can't make spans from collection with only 1 element!")
            return PairedCollection([(__init_val, __init_val)])
        __f = Rangifier(__init_val)
        return PairedCollection(map(__f, _tail))
    

    def rangify(self) -> PairedCollection[tuple[T1, T2], tuple[T1, T2]]:
        """Deprecated version of `as_spans()`

        Returns:
            PairedCollection[T, T]: New PairedCollection of paired spans.
        """        
        return self.as_spans()