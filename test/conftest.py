from typing import Any, Callable, Iterable, Tuple

import pytest

from trent.collection_core import Collection
from trent.interface import paired_seq, seq
from trent.paired_coll import PairedCollection


@pytest.fixture
def coll_factory() -> Callable[[Iterable], Collection]:
    """Factory that produces lazy collections from lists."""

    def factory(items: Iterable) -> Collection:
        return seq(list(items))

    return factory


@pytest.fixture
def pairs_factory() -> Callable[[Iterable[Tuple]], PairedCollection]:
    """Factory that produces paired collections from pair tuples."""

    def factory(pairs: Iterable[Tuple]) -> PairedCollection:
        return paired_seq(list(pairs))

    return factory