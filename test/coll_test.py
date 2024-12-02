from trent.coll import icoll, persistent_coll

def _rng(n: int):
    return range(n)

def _double(n: int|float):
    return n*n

def _fact(n: int):
    assert n >= 0
    if n <= 1:
        return 1
    res = 1
    for i in range(1, n):
        res += i
    return res

# ========================================================

def test_mapping_1():
    c = icoll([1, 2, 3, 4])
    res = c.map(lambda x: x*x)
    
    assert list(res) == [1, 4, 9, 16]


def test_mapping_2():
    c = icoll([1, 2, 3])
    res = list(c.map(str))
    assert isinstance(res[0], str)
    assert res == ['1', '2', '3']

def test_pmap_1():
    c = icoll(range(100))
    res = c.pmap(_fact)
    assert list(res) == [_fact(i) for i in range(100)]


def test_pmap_2():
    c = icoll(range(100))
    res = c.pmap_(_fact, 2)
    assert list(res) == [_fact(i) for i in range(100)]


def test_filter_1():
    def _isodd(n: int):
        return n % 2
    c = icoll(range(10))
    res = list(c.filter(_isodd))
    assert res == [1, 3, 5, 7, 9]


def test_filter_2():
    def _iseven(n: int):
        return n % 2 == 0
    c = icoll(range(10))
    res = list(c.filter(_iseven))
    assert res == [0, 2, 4, 6, 8]


def test_remove():
    def _isodd(n: int):
        return n % 2
    c = icoll(range(10))
    res = list(c.remove(_isodd))
    assert res == [0, 2, 4, 6, 8]


def test_remove_none():
    c = icoll([1,2,3,4,None,6,None,8])
    res = list(c.remove_none())
    assert res == [1,2,3,4,6,8]


def test_mapcat():
    c = icoll([2, 3, 4])
    res = c.mapcat(_rng)
    assert list(res) == [0,1, 0,1,2, 0,1,2,3]


def test_mapcat_2():
    c = icoll([])
    res = c.mapcat(_rng)
    assert list(res) == []


def test_catmap():
    c = icoll([[1, 2], [3, 4, 5]])
    res = c.catmap(_double)
    assert list(res) == [1, 4, 9, 16, 25]


def test_unique():
    c = icoll([1, 2, 3, 2, 1, 6, 10, 10, 1])
    res = c.unique()
    assert list(res) == [1, 2, 3, 6, 10]


def test_distinct_by():
    def _f(s: str) -> str:
        if len(s) < 3:
            return s
        return s[0:2]
    c = icoll(['football', 'foobar', 'foony', 'barber', 'barbaz'])
    res = c.distinct_by(_f)
    assert list(res) == ['football', 'barber']



def test_take():
    c = icoll(range(10000))
    res = c.take(5)
    assert list(res) == [0, 1, 2, 3, 4]


def test_takewhile():
    c = icoll(range(10000))
    res = c.takewhile(lambda n: n < 6)
    assert list(res) == [0, 1, 2, 3, 4, 5]


def test_cat():
    c = icoll([[1, 2, 3], [4, 5]])
    res = c.cat()
    assert list(res) == [1, 2, 3, 4, 5]



def test_persistent_coll():
    c = persistent_coll([1,2,3])
    res = c.map(lambda x: x*x).map(lambda x: x*x)
    
    assert list(res) == [1, 16, 81]
    assert list(res) == [1, 16, 81]