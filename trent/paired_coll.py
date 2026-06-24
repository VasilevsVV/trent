from __future__ import annotations
from typing import TYPE_CHECKING

from typing import Any, Callable, Dict, Generic, Iterable, TypeVar, Tuple, overload
from trent.func import identity
from trent.nth import first, first_, second, second_
from trent.collection_base import C, R1, R2, T1, T2, CollectionBase

if TYPE_CHECKING:
    from trent.coll import Collection


class PairedCollection(CollectionBase[Tuple[T1, T2]], Iterable[Tuple[T1, T2]]):


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