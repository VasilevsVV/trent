from typing import Sequence
from trent.coll import icoll


def first(seq: Sequence):
    return seq[0]

def second(seq: Sequence):
    return seq[1]


def test_group_by_to_dict_1():
    def __mod10(val: int):
        return val // 10
    c = icoll(range(30))
    res = c.group_by_to_dict(__mod10)
    assert res == {
                    0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    1: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                    2: [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
                    }


def test_group_by_to_dict_2():
    c = icoll([(1, 10), (1, 15), (2, 21), (2, 27)])
    res = c.group_by_to_dict(first)
    assert res == {1: [(1, 10), (1, 15)],
                   2: [(2, 21), (2, 27)]}


def test_group_by_to_dict_3():
    c = icoll([(1, 10), (1, 15), (2, 21), (2, 27)])
    res = c.group_by_to_dict(first, second)
    assert res == {1: [10, 15],
                   2: [21, 27]}


def test_group_by_1():
    def __mod10(val: int):
        return val // 10
    c = icoll(range(30))
    res = c.group_by_to_dict(__mod10)
    assert res == {
                    0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    1: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                    2: [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
                    }