# ======================================================
#           TEST map_to_pair

from trent.interface import seq
from trent.paired_coll import paired_icoll


def test_map_to_pair():
    c = seq(range(3))
    c = c.map_to_pair(str)
    assert isinstance(c, paired_icoll)
    assert c.to_list() == [('0', 0), ('1', 1), ('2', 2)]


def foo(t: tuple[str, int]) -> tuple[str, int]:
    return (t[0], t[1] + 10)

if __name__ == '__main__':
    c = seq(range(3))
    # print(c.to_list())
    c = c.map_to_pair(str)
    c = c.append(('4', 4))
    # print(c.to_list())
    c = c.extend([('5', 5), ('6', 6)])
    c = c.map(foo)

    print(c)
    print(c.to_list())