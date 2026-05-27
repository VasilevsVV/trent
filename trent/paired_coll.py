# from __future__ import annotations
# from typing import TYPE_CHECKING

from typing import Any, Callable, Dict, Generic, Iterable, TypeVar, Tuple, overload
from trent.func import identity
from trent.nth import first, first_, second, second_
from trent.collection_base import C, R1, R2, T1, T2, icoll_base

# if TYPE_CHECKING:
#     from coll import icoll

# T1 = TypeVar('T1')
# T2 = TypeVar('T2')

# R1 = TypeVar('R1')
# R2 = TypeVar('R2')


class paired_icoll(icoll_base[Tuple[T1, T2]], Iterable[Tuple[T1, T2]]):
    @overload
    def pairmap(self, f:Callable[[T1, T2], Tuple[R1, R2]]) -> "paired_icoll[R1, R2]": ...
    @overload
    def pairmap(self, f:Callable[[T1, T2], R1]) -> icoll_base[R1]: ...

    def pairmap(self, f:Callable[[T1, T2], Any]): # type: ignore
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
        if self.empty:
            return icoll_base(self).map(_f) # just for consistency.
        _h = _f(self.head) # type: ignore
        if (
            isinstance(_h, Tuple) 
            and len(_h) == 2
        ):
            return paired_icoll(map(_f, self.collection))
        return icoll_base(self).map(_f)
    

    def group_by(
            self, 
            f:Callable[[Tuple[T1, T2]], R1], 
            val_fn: Callable[[Tuple[T1, T2]], R2] = identity
            ) -> "paired_icoll[R1, list[R2]]":
        d = self.group_by_to_dict(f, val_fn)
        return paired_icoll(d.items())


    def __repr__(self) -> str:
        return f'paired_coll({self._coll})'



def foo(name: str, val: int):
    return f'{name}: {val}'


def bar(name: str, val: int):
    return (val, name)

if __name__ == '__main__':
    c = paired_icoll([('a', 1), ('b', 2)])
    print(c)
    print(c.to_list())
    print(c.pairmap(foo))
    res = c.pairmap(bar)
    print(res)
    print(res.head)
    print(res.to_list())