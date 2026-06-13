from __future__ import annotations
from typing import TYPE_CHECKING

from typing import (
    Callable,
    Iterable,
    Tuple,
)


from trent.collection_base import T, T1, T2, CollectionBase
from trent.func import identity


if TYPE_CHECKING:
    from paired_coll import PairedCollection



class Collection(CollectionBase, Iterable[T]):
    def map_to_pair(self, f_key: Callable[[T], T1], f_val: Callable[[T], T2] = identity) -> PairedCollection[T1, T2]:
        from trent.paired_coll import PairedCollection
        def __pair(val: T) -> Tuple[T1, T2]:
            return (f_key(val), f_val(val))
        return PairedCollection(self.map(__pair))
    

    def group_by(self, f:Callable[[T], T1], val_fn: Callable[[T], T2] = identity) -> PairedCollection[T1, list[T2]]:
        from trent.paired_coll import PairedCollection
        d = self.group_by_to_dict(f, val_fn)
        return PairedCollection(d.items())