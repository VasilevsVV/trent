from pprint import pprint

from trent.func import identity
from trent.interface import seq, map_to_pair
from trent.nth import first, first_, second


def test_combined_colls_1():
    c = (
        seq(range(10))
        .map_to_pair(lambda x: x % 3)
        .pairmap_to_pair(lambda x,y: (f'group_{x}', y))
        .group_by(first_, second)
    )
    res = dict(c)
    assert res == {
        'group_0': [0, 3, 6, 9],
        'group_1': [1, 4, 7],
        'group_2': [2, 5, 8]
    }


def test_combined_colls_2():
    c = (
        seq(range(10))
        .mapcat(lambda x: range(x))
        .group_by(identity)
        .pairmap_to_pair(lambda x,lst: (x, len(lst)))
        .to_dict()
    )
    assert c == {0: 9, 1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}


def _join(res: str, vals: tuple[int, int]):
        if res.strip() == '':
            return f'{vals[0]}: {vals[1]}'
        return res + f', {vals[0]}: {vals[1]}'

def test_combined_colls_3():
    c = (
        seq(range(10))
        .mapcat(lambda x: range(x))
        .group_by(identity)
        .pairmap_to_pair(lambda x,lst: (x, len(lst)))
        .reduce(_join, '')
    )
    assert c == '0: 9, 1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1'