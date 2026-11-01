from typing import Iterable

from trent.coll import CollectionImpl
from trent.exceptions import EmptyCollectionException
from trent.func import identity
from trent.interface import (
    cat,
    catmap,
    cfilter,
    cmap,
    groupcoll,
    groupmap,
    map_to_pair,
    mapcat,
    pairmap,
    pmap,
    pmap_,
    rangify,
    seq,
)


def test_seq():
    c = seq(range(3))
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [0,1,2]


def test_seq_none():
    c = seq(None)
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == []


def test_seq_dict():
    c = seq({'a': 1, 'b': 2})
    assert isinstance(c, CollectionImpl)
    items = c.to_list()
    assert ('a', 1) in items
    assert ('b', 2) in items


def test_seq_list():
    c = seq([1, 2, 3])
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [1, 2, 3]


def _f1(x: int) -> int:
    return x * 10

def test_cmap():
    c = cmap(_f1, range(3))
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [0,10,20]


def _pr1(x: int) -> bool:
    return x % 3 == 0

def test_cfilter():
    c = cfilter(_pr1, range(10))
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [0,3,6,9]


def test_cat():
    c = cat([(1,2), (3,4), (5,6)])
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [1,2,3,4,5,6]


def _f2(x: int) -> Iterable[int]:
    return range(x)

def test_mapcat():
    c = mapcat(_f2, range(5))
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [0,0,1,0,1,2,0,1,2,3]


# ======================================================
#           TEST pmap / pmap_


def _double(x):
    return x * 2


def test_pmap_1():
    c = pmap(_double, [1, 2, 3])
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [2, 4, 6]


def test_pmap_empty():
    c = pmap(_double, [])
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == []


def test_pmap_1_threads():
    c = pmap_(_double, [1, 2, 3], threads=2)
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [2, 4, 6]



# ======================================================
#           TEST catmap


def _expand(x):
    return [x, x * 10]


def test_catmap_1():
    # catmap semantics: "flatten then map" (see USER_GUIDE.md).
    # [[1], [2]] is flattened to [1, 2], then each element is mapped by _expand.
    # Result is NOT flattened (that is mapcat).
    c = catmap(_expand, [[1], [2]])
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [[1, 10], [2, 20]]


def test_catmap_empty():
    def _expand_empty(x):
        return [x]
    c = catmap(_expand_empty, [])
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == []


# ======================================================
#           TEST pairmap


def test_pairmap_1():
    def __add(n1: int, n2:int):
        return n1 + n2
    c = pairmap(__add, [(1,2), (3,4), (5,6)])
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [3, 7, 11]


# ======================================================
#           TEST groupcoll / groupmap


def test_groupcoll_1():
    c = groupcoll([(1, [10, 20]), (2, [30, 40])])
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == [(1, 10), (1, 20), (2, 30), (2, 40)]


def test_groupmap_1():
    def __add(id: int, val: int):
        return f'{id}:{val}'
    c = groupmap(__add, [(1, [10, 20]), (2, [30, 40])])
    assert isinstance(c, CollectionImpl)
    assert c.to_list() == ['1:10', '1:20', '2:30', '2:40']


# ======================================================
#           TEST map_to_pair


def test_map_to_pair_1():
    c = map_to_pair([1, 2, 3], str)
    assert c.to_list() == [('1', 1), ('2', 2), ('3', 3)]


def test_map_to_pair_2():
    c = map_to_pair([1, 2, 3], str, str)
    assert c.to_list() == [('1', '1'), ('2', '2'), ('3', '3')]


# ======================================================
#           TEST rangify


def test_rangify_1():
    c = rangify([1, 2, 3])
    assert c.to_list() == [(1, 2), (2, 3)]


def test_rangify_empty():
    c = rangify([])
    assert c.to_list() == []


def test_rangify_single():
    c = rangify([1])
    assert c.to_list() == [(1, 1)]


if __name__ == '__main__':
    c = mapcat(_f2, range(5))
    assert isinstance(c, CollectionImpl)
    # assert c.to_list() == [0,0,1,0,1,2,0,1,2,3,0,1,2,3,4]
    print(c.to_list())