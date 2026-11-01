import pytest

import trent


# ======================================================
#           TEST module exports


def test_collection_exported():
    assert hasattr(trent, 'Collection')


def test_collection_impl_exported():
    assert hasattr(trent, 'CollectionImpl')


def test_paired_collection_exported():
    assert hasattr(trent, 'PairedCollection')


# ======================================================
#           TEST seq/coll/icoll


def test_seq_exported():
    assert hasattr(trent, 'seq')


def test_coll_exported():
    assert hasattr(trent, 'coll')


def test_icoll_exported():
    assert hasattr(trent, 'icoll')


def test_coll_is_seq():
    assert trent.coll is trent.seq


def test_icoll_is_seq():
    assert trent.icoll is trent.seq


# ======================================================
#           TEST cmap/cfilter


def test_cmap_exported():
    assert hasattr(trent, 'cmap')


def test_cfilter_exported():
    assert hasattr(trent, 'cfilter')


# ======================================================
#           TEST pmap/pmap_


def test_pmap_exported():
    assert hasattr(trent, 'pmap')


def test_pmap_exported_2():
    assert hasattr(trent, 'pmap_')


# ======================================================
#           TEST cat/mapcat/catmap


def test_cat_exported():
    assert hasattr(trent, 'cat')


def test_mapcat_exported():
    assert hasattr(trent, 'mapcat')


def test_catmap_exported():
    assert hasattr(trent, 'catmap')


# ======================================================
#           TEST pairmap/map_to_pair


def test_pairmap_exported():
    assert hasattr(trent, 'pairmap')


def test_map_to_pair_exported():
    assert hasattr(trent, 'map_to_pair')


# ======================================================
#           TEST groupcoll/groupmap/rangify


def test_groupcoll_exported():
    assert hasattr(trent, 'groupcoll')


def test_groupmap_exported():
    assert hasattr(trent, 'groupmap')


def test_rangify_exported():
    assert hasattr(trent, 'rangify')


# ======================================================
#           TEST nth accessors


def test_first_exported():
    assert hasattr(trent, 'first')


def test_first_strict_exported():
    assert hasattr(trent, 'first_')


def test_second_exported():
    assert hasattr(trent, 'second')


def test_second_strict_exported():
    assert hasattr(trent, 'second_')


def test_third_exported():
    assert hasattr(trent, 'third')


# ======================================================
#           TEST func utils


def test_gtr_exported():
    assert hasattr(trent, 'gtr')


def test_gtr_strict_exported():
    assert hasattr(trent, 'gtr_')


def test_identity_exported():
    assert hasattr(trent, 'identity')


def test_isnone_exported():
    assert hasattr(trent, 'isnone')


# ======================================================
#           TEST exceptions


def test_missing_value_exception_exported():
    assert hasattr(trent, 'MissingValueException')


def test_empty_collection_exception_exported():
    assert hasattr(trent, 'EmptyCollectionException')


# ======================================================
#           TEST __all__ completeness


def test_all_exports():
    assert isinstance(trent.__all__, list)
    assert len(trent.__all__) == 30


def test_all_names_are_attributes():
    for name in trent.__all__:
        assert hasattr(trent, name), f"Missing attribute: {name}"
