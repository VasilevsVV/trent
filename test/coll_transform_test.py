from typing import Iterable
from trent.coll import icoll


def test_concat():
    c = icoll(range(4))
    res = c.concat([4, 5])
    assert list(res) == [0, 1, 2, 3, 4, 5]


def test_append():
    c = icoll(range(4))
    res = c.append(4)
    assert list(res) == [0, 1, 2, 3, 4]


def test_append__2():
    c = icoll(list(range(4)))
    assert c.collection == [0, 1, 2, 3]
    c.append_(4)
    assert list(c) == [0, 1, 2, 3, 4]


def test_extend():
    c = icoll(range(4))
    res = c.extend([4, 5])
    assert list(res) == [0, 1, 2, 3, 4, 5]


def test_extend__2():
    c = icoll(list(range(4)))
    assert c.collection == [0, 1, 2, 3]
    c.extend_([4, 5])
    assert list(c) == [0, 1, 2, 3, 4, 5]


def test_cons():
    c = icoll(range(4))
    res = c.cons(10)
    assert list(res) == [10, 0, 1, 2, 3]


def test_cons__2():
    c = icoll(list(range(4)))
    assert c.collection == [0, 1, 2, 3]
    c.cons_(10)
    assert list(c) == [10, 0, 1, 2, 3]


def test_add_oper_1():
    c = icoll(range(10))
    res = c + range(10, 20)
    assert list(res) == list(range(20))


def test_add_oper_2():
    c = icoll(range(10))
    c += range(10, 20)
    assert list(c) == list(range(20))


def test_to_list():
    c = icoll(range(10))
    assert c.to_list() == list(range(10))


def test_collect_1():
    c = icoll(range(10))
    res = c.collect()
    assert res == list(range(10))


def test_collect_2():
    c = icoll(range(10))
    assert c.collect(str) == str(list(range(10)))


def test_collect_3():
    def __foo(lst: Iterable[int]):
        return lst[0:3]
    c = icoll(range(10))
    assert c.collect(__foo) == [0, 1, 2]