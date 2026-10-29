import pytest

from trent.func import identity, getter, gtr, gtr_, isnone, NV


# ======================================================
#           TEST identity


def test_identity_1():
    assert identity(42) == 42


def test_identity_2():
    assert identity("hello") == "hello"


def test_identity_3():
    assert identity(None) is None


def test_identity_4():
    assert identity([]) == []


def test_identity_5():
    assert identity({}) == {}


# ======================================================
#           TEST getter


def test_getter_1():
    f = getter('foo', 'default')
    assert f({'foo': 'bar'}) == 'bar'


def test_getter_2():
    f = getter('missing', 'default')
    assert f({}) == 'default'


def test_getter_3():
    f = getter('nested', None)
    assert f({'nested': {'a': 1}}) == {'a': 1}


def test_getter_4():
    f = getter('key')
    assert f({}) is None


# ======================================================
#           TEST gtr


def test_gtr_1():
    f = gtr('foo', 'default')
    assert f({'foo': 'bar'}) == 'bar'


def test_gtr_2():
    f = gtr('missing', 'default')
    assert f({}) == 'default'


def test_gtr_3():
    f = gtr('key')
    assert f({}) is None


def test_gtr_4():
    assert gtr('a', 1)({'a': 1}) == 1


# ======================================================
#           TEST gtr_


def test_gtr_strict_1():
    f = gtr_('foo', str)
    assert f({'foo': 'bar'}) == 'bar'


def test_gtr_strict_2():
    f = gtr_('foo', int)
    assert f({'foo': 42}) == 42


def test_gtr_strict_raises_missing():
    f = gtr_('missing', int)
    with pytest.raises(Exception):
        f({})


def test_gtr_strict_raises_empty():
    f = gtr_('key', str)
    with pytest.raises(Exception):
        f({})


# ======================================================
#           TEST isnone


def test_isnone_none():
    assert isnone(None) is True


def test_isnone_not_none():
    assert isnone(0) is False


def test_isnone_empty_string():
    assert isnone("") is False


def test_isnone_zero():
    assert isnone(0) is False


def test_isnone_false():
    assert isnone(False) is False


# ======================================================
#           TEST NV sentinel


def test_nv_is_no_value():
    from trent.nth import __no_value
    assert isinstance(NV, __no_value)
