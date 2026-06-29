import asyncio
import time

from trent.interface import seq


def test_async_partmap_1():
    c = seq([range(100), range(100, 200)])
    res = c.async_partmap(lambda n: n * 10)
    __res_val = [list(range(0, 1000, 10)), list(range(1000, 2000, 10))]
    assert list(res) == __res_val


def test_async_partmap_2():
    c = seq([range(100), range(100, 200)])
    res = c.async_partmap_(lambda n: n * 10, 4)
    __res_val = [list(range(0, 1000, 10)), list(range(1000, 2000, 10))]
    assert list(res) == __res_val

def test_async_partmap_3():
    c = seq([range(100), range(100, 200)])
    res = c.async_partmap(lambda n: n * 10, threads=4)
    __res_val = [list(range(0, 1000, 10)), list(range(1000, 2000, 10))]
    assert list(res) == __res_val


def test_async_foreach_1():
    res = []
    def _foo(x: int):
        res.append(x*2)
    seq(range(5)).async_foreach(_foo, 2)
    assert set(res) == set([0, 2, 4, 6, 8])
