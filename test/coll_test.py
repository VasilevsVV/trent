from trent.coll import coll


def test_mapping_1():
    c = coll([1, 2, 3, 4])
    res = c.map(lambda x: x*x)
    
    assert list(res) == [1, 4, 9, 16]


def test_mapping_2():
    c = coll([1, 2, 3])
    res = list(c.map(str))
    assert isinstance(res[0], str)
    assert res == ['1', '2', '3']


def test_filter_1():
    def _isodd(n: int):
        return n % 2
    c = coll(range(10))
    res = list(c.filter(_isodd))
    assert res == [1, 3, 5, 7, 9]


def test_filter_2():
    def _iseven(n: int):
        return n % 2 == 0
    c = coll(range(10))
    res = list(c.filter(_iseven))
    assert res == [0, 2, 4, 6, 8]