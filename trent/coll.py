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
    from trent.paired_coll import PairedCollection



class Collection(CollectionBase, Iterable[T]):
    def map_to_pair(self, f_key: Callable[[T], T1], f_val: Callable[[T], T2] = identity) -> PairedCollection[T1, T2]:
        """Map sequence to a PairedCollection of tuples, using 2 provided functions.
        
        Resulting tuples created as: `(f_key(value), f_val(value))`

        Args:
            f_key (Callable[[T], T1]): function to generate first value in pair (tuple).
            f_val (Callable[[T], T2], optional): function to generate second value in pair (tuple). Defaults to identity.

        Returns:
            PairedCollection[T1, T2]: New PairedCollection, where T1,T2 - types returned by f_key & f_val
        
        Examples:
        Using only `f_key` (retains the original element as the value via `identity`):
        >>> words = Collection(["apple", "pear"])
        >>> words.map_to_pair(len).to_list()
        [(5, 'apple'), (4, 'pear')]

        Providing both `f_key` and `f_val` to transform both elements of the tuple:
        >>> nums = Collection([1, 2, 3])
        >>> nums.map_to_pair(lambda x: f"id_{x}", lambda x: x * 10).to_list()
        [('id_1', 10), ('id_2', 20), ('id_3', 30)]
        """         
        from trent.paired_coll import PairedCollection
        def __pair(val: T) -> Tuple[T1, T2]:
            return (f_key(val), f_val(val))
        return PairedCollection(self.map(__pair))
    

    def group_by(self, f:Callable[[T], T1], val_fn: Callable[[T], T2] = identity) -> PairedCollection[T1, list[T2]]:
        """Group elements by a result of function `f`.
        WARNING: This operatios is NOT LAZY (requires to evalueate all elements of Collection.) 
        It may require a lot of RAM.

        Args:
            f (Callable[[T], T1]): Function to be used as a grouping key generator
            val_fn (Callable[[T], T2], optional): Function to map values of groups. Defaults to identity.

        Returns:
            PairedCollection[T1, list[T2]]: New grouped PairedCollection. 
            Where T1 - type returned by function `f`. And T2 - type returned by `val_fn`
        
        Examples:
        Grouping elements by a key extractor function (with `val_fn` defaulting to identity):
        >>> words = Collection(["apple", "pear", "banana", "kiwi"])
        >>> words.group_by(len).to_list()
        [(5, ['apple']), (4, ['pear', 'kiwi']), (6, ['banana'])]

        Grouping structured objects and extracting/transforming elements using `val_fn`:
        >>> logs = Collection([
        ...     {"env": "prod", "msg": "Error A"},
        ...     {"env": "test", "msg": "Debug B"},
        ...     {"env": "prod", "msg": "Error C"}
        ... ])
        >>> logs.group_by(lambda x: x["env"], val_fn=lambda x: x["msg"]).to_list()
        [('prod', ['Error A', 'Error C']), ('test', ['Debug B'])]
        """        
        from trent.paired_coll import PairedCollection
        d = self.group_by_to_dict(f, val_fn)
        return PairedCollection(d.items())
    

    def as_spans(self, *, fail_if_single: bool = False) -> PairedCollection[T, T]:
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
    

    def rangify(self) -> PairedCollection[T, T]:
        """Deprecated version of `as_spans()`

        Returns:
            PairedCollection[T, T]: New PairedCollection of paired spans.
        """        
        return self.as_spans()