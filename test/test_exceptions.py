import pytest

from trent.exceptions import MissingValueException, EmptyCollectionException


# ======================================================
#           TEST MissingValueException


def test_missing_value_exception_str_1():
    exc = MissingValueException([1, 2, 3], 'first')
    assert str(exc) == 'Missing first for value: [1, 2, 3]'


def test_missing_value_exception_str_2():
    exc = MissingValueException([], 'second')
    assert str(exc) == 'Missing second for value: []'


def test_missing_value_exception_str_3():
    exc = MissingValueException(None, 'nth')
    assert str(exc) == 'Missing nth for value: None'


def test_missing_value_exception_attrs():
    exc = MissingValueException({'a': 1}, 'key')
    assert exc._value == {'a': 1}
    assert exc._fn_name == 'key'


def test_missing_value_exception_is_exception():
    exc = MissingValueException(None, 'test')
    assert isinstance(exc, Exception)


# ======================================================
#           TEST EmptyCollectionException


def test_empty_collection_exception_str_1():
    exc = EmptyCollectionException('on head')
    assert 'Collection is empty!' in str(exc)
    assert 'on head' in str(exc)


def test_empty_collection_exception_str_2():
    exc = EmptyCollectionException('on tail')
    assert 'Collection is empty!' in str(exc)


def test_empty_collection_exception_str_3():
    exc = EmptyCollectionException('on first')
    assert 'Collection is empty!' in str(exc)


def test_empty_collection_exception_is_exception():
    exc = EmptyCollectionException('test')
    assert isinstance(exc, Exception)
