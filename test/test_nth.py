import pytest

from trent.coll import CollectionImpl
from trent.exceptions import MissingValueException
from trent.func import identity
from trent.interface import seq
from trent.nth import first, first_, second, second_, third, nth, nth_


# ======================================================
#           TEST first


def test_first_1():
    assert first([1, 2, 3]) == 1


def test_first_2():
    assert first(range(5)) == 0


def test_first_3():
    c = seq([10, 20, 30])
    assert first(c) == 10


def test_first_4():
    assert first([42]) == 42


def test_first_5():
    assert first([]) is None


def test_first_6():
    assert first(None) is None


# ======================================================
#           TEST second


def test_second_1():
    assert second([1, 2, 3]) == 2


def test_second_2():
    assert second(range(5)) == 1


def test_second_3():
    c = seq([10, 20, 30])
    assert second(c) == 20


def test_second_4():
    assert second([42]) is None


def test_second_5():
    assert second([]) is None


# ======================================================
#           TEST third


def test_third_1():
    assert third([1, 2, 3]) == 3


def test_third_2():
    assert third(range(5)) == 2


def test_third_3():
    c = seq([10, 20, 30, 40])
    assert third(c) == 30


def test_third_4():
    assert third([1, 2]) is None


def test_third_5():
    assert third([]) is None


# ======================================================
#           TEST nth


def test_nth_1():
    assert nth([1, 2, 3], 0) == 1


def test_nth_2():
    assert nth([1, 2, 3], 1) == 2


def test_nth_3():
    assert nth([1, 2, 3], 2) == 3


def test_nth_4():
    assert nth([1, 2, 3], 5) is None


def test_nth_5():
    assert nth([], 0) is None


def test_nth_6():
    assert nth(range(10), 9) == 9


# ======================================================
#           TEST first_ (strict)


def test_first_strict_1():
    assert first_([1, 2, 3]) == 1


def test_first_strict_2():
    assert first_(range(5)) == 0


def test_first_strict_raises_empty():
    with pytest.raises(MissingValueException):
        first_([])


def test_first_strict_raises_missing():
    with pytest.raises(MissingValueException):
        first_(())


# ======================================================
#           TEST second_ (strict)


def test_second_strict_1():
    assert second_([1, 2, 3]) == 2


def test_second_strict_2():
    assert second_([1, 2]) == 2


def test_second_strict_raises_empty():
    with pytest.raises(MissingValueException):
        second_([])


def test_second_strict_raises_single():
    with pytest.raises(MissingValueException):
        second_([1])


# ======================================================
#           TEST nth_ (strict)


def test_nth_strict_1():
    assert nth_([1, 2, 3], 2) == 3


def test_nth_strict_2():
    assert nth_([1, 2, 3], 0) == 1


def test_nth_strict_raises_empty():
    with pytest.raises(MissingValueException):
        nth_([], 0)


def test_nth_strict_raises_missing():
    with pytest.raises(MissingValueException):
        nth_([1, 2], 5)


# ======================================================
#           TEST with CollectionImpl


def test_nth_via_collection_1():
    c = CollectionImpl([10, 20, 30])
    assert first(c) == 10
    assert second(c) == 20
    assert third(c) == 30


def test_nth_via_collection_strict():
    c = CollectionImpl([10, 20, 30])
    assert first_([10, 20, 30]) == 10
    assert second_([10, 20, 30]) == 20
    assert third([10, 20, 30]) == 30
