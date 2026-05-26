from typing import Iterable

from trent.coll import icoll
from trent.interface import cat, cfilter, cmap, mapcat, seq


def test_seq():
    c = seq(range(3))
    assert isinstance(c, icoll)
    assert c.to_list() == [0,1,2]


def _f1(x: int) -> int:
    return x * 10

def test_cmap():
    c = cmap(_f1, range(3))
    assert isinstance(c, icoll)
    assert c.to_list() == [0,10,20]


def _pr1(x: int) -> bool:
    return x % 3 == 0

def test_cfilter():
    c = cfilter(_pr1, range(10))
    assert isinstance(c, icoll)
    assert c.to_list() == [0,3,6,9]


def test_cat():
    c = cat([(1,2), (3,4), (5,6)])
    assert isinstance(c, icoll)
    assert c.to_list() == [1,2,3,4,5,6]


def _f2(x: int) -> Iterable[int]:
    return range(x)

def test_mapcat():
    c = mapcat(_f2, range(5))
    assert isinstance(c, icoll)
    assert c.to_list() == [0,0,1,0,1,2,0,1,2,3]



if __name__ == '__main__':
    c = mapcat(_f2, range(5))
    assert isinstance(c, icoll)
    # assert c.to_list() == [0,0,1,0,1,2,0,1,2,3,0,1,2,3,4]
    print(c.to_list())