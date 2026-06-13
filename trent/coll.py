from __future__ import annotations
from typing import TYPE_CHECKING

from typing import (
    Callable,
    Iterable,
    Tuple,
)


from trent.coll_aux import Rangifier
from trent.collection_base import T, T1, T2, CollectionBase
from trent.exceptions import EmptyCollectionException, MissingValueException
from trent.func import identity
from trent.nth import first_


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
    

    def rangify(self) -> PairedCollection[T, T]:
        from trent.paired_coll import PairedCollection
        try:
            __init_val = self.head
        except EmptyCollectionException:
            raise EmptyCollectionException("Can't `rangify` an empty collection!")
        __f = Rangifier(__init_val)
        return PairedCollection(map(__f, self.tail()))