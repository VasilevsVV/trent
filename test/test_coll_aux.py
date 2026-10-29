import pytest

from trent.coll_aux import DistinctFilter, Rangifier, PartCounter, PartByCounter


# ======================================================
#           TEST DistinctFilter


def test_distinct_filter_basic():
    f = DistinctFilter(lambda x: x)
    assert f(1) is True
    assert f(1) is False
    assert f(2) is True
    assert f(2) is False


def test_distinct_filter_callable():
    f = DistinctFilter(lambda x: x % 3)
    assert f(1) is True   # 1 % 3 = 1
    assert f(4) is False  # 4 % 3 = 1 (duplicate)
    assert f(2) is True   # 2 % 3 = 2
    assert f(5) is False  # 5 % 3 = 2 (duplicate)


def test_distinct_filter_string():
    f = DistinctFilter(lambda x: x.upper())
    assert f('a') is True
    assert f('A') is False
    assert f('b') is True


def test_distinct_filter_empty():
    f = DistinctFilter(lambda x: x)
    assert f(None) is True
    assert f(None) is False


def test_distinct_filter_accumulates():
    f = DistinctFilter(lambda x: x)
    results = [f(x) for x in [1, 2, 1, 3, 2, 4]]
    assert results == [True, True, False, True, False, True]


# ======================================================
#           TEST Rangifier


def test_rangifier_basic():
    r = Rangifier(0)
    assert r(1) == (0, 1)
    assert r(2) == (1, 2)
    assert r(3) == (2, 3)


def test_rangifier_string():
    r = Rangifier('a')
    assert r('b') == ('a', 'b')
    assert r('c') == ('b', 'c')


def test_rangifier_accumulates():
    r = Rangifier(10)
    pairs = [r(x) for x in [20, 30, 40]]
    assert pairs == [(10, 20), (20, 30), (30, 40)]


# ======================================================
#           TEST PartCounter


def test_part_counter_basic():
    c = PartCounter(3)
    assert c() == 0
    assert c() == 0
    assert c() == 0
    assert c() == 1
    assert c() == 1
    assert c() == 1
    assert c() == 2


def test_part_counter_small():
    c = PartCounter(2)
    assert c() == 0
    assert c() == 0
    assert c() == 1
    assert c() == 1
    assert c() == 2


def test_part_counter_ignores_args():
    c = PartCounter(2)
    assert c('ignore') == 0
    assert c(123) == 0
    assert c(None) == 1


# ======================================================
#           TEST PartByCounter


def test_part_by_counter_basic():
    c = PartByCounter(lambda x: x > 5)
    assert c(1) == 0
    assert c(3) == 0
    assert c(6) == 1
    assert c(7) == 2
    assert c(2) == 2


def test_part_by_counter_string():
    c = PartByCounter(lambda x: x.startswith('A'))
    assert c('A') == 1
    assert c('B') == 1
    assert c('A') == 2


def test_part_by_counter_no_match():
    c = PartByCounter(lambda x: False)
    assert c(1) == 0
    assert c(2) == 0
    assert c(3) == 0
