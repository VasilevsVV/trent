from pprint import pprint

from trent.interface import seq, map_to_pair
from trent.nth import first, first_, second


def test_combined_colls_1():
    c = (
        seq(range(10))
        .map_to_pair(lambda x: x % 3)
        .pairmap(lambda x,y: (f'group_{x}', y))
        .group_by(first_, second)
    )
    res = dict(c)
    assert res == {
        'group_0': [0, 3, 6, 9],
        'group_1': [1, 4, 7],
        'group_2': [2, 5, 8]
    }


if __name__ == '__main__':
    c = (
        seq(range(10))
        .map_to_pair(lambda x: x % 3)
        .pairmap(lambda x,y: (f'group_{x}', y))
        .group_by(first_, second)
        .persist()
        # .to_list()
    )
    pprint(c)
    # pprint(c.to_list())
    pprint(dict(c))