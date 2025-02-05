from typing import Optional, Sequence
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


def test_rangify():
    c = icoll(range(10))
    res = c.rangify()
    assert list(res) == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]



def test_pairmap_1():
    def __add(n1: int, n2:int):
        return n1 + n2
    c = icoll([(1,2), (3,4), (5,6)])
    res = c.pairmap(__add)
    assert list(res) == [3, 7, 11]


def test_pairmap_2():
    def __mod10(val: int):
        return val // 10
    def __add(id: int, lst: list[int]):
        sum = 0
        for i in lst:
            sum += i
        return f'{id}->{sum}'
    c = icoll(range(30))
    res = c.group_by(__mod10).pairmap(__add)
    assert res.to_list() == ['0->45', '1->145', '2->245']


def test_pairmap_3():
    def __add(n1: int, n2: Optional[int]):
        if n2 is None:
            return n1
        return n1 + n2
    c = icoll([(1,2), (3, ), (5,6)])
    res = c.pairmap(__add)
    assert list(res) == [3, 3, 11]


def test_groupmap():
    def __mod3(val: int):
        return val % 3
    def __add(id: int, val: int):
        return f'{id}:{val}'
    c = icoll(range(10))
    res = c.group_by(__mod3).groupmap(__add)
    assert list(res) == ['0:0', '0:3', '0:6', '0:9', '1:1', '1:4', '1:7', '2:2', '2:5', '2:8']
    


if __name__ == '__main__':
    test_pairmap_2()