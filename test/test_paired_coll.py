from trent.func import identity
from trent.interface import paired_seq, seq
from trent.paired_coll import PairedCollection



# ======================================================
#           TEST map_to_pair


def test_map_to_pair():
    c = seq(range(3))
    c = c.map_to_pair(str)
    assert isinstance(c, PairedCollection)
    assert c.to_list() == [('0', 0), ('1', 1), ('2', 2)]


def test_pairmap_to_pair():
    c = seq(range(3))
    c = c.map_to_pair(identity, str)
    assert isinstance(c, PairedCollection)
    assert c.to_list() == [(0, '0'), (1, '1'), (2, '2')]


def test_paired_seq_1():
    c = paired_seq([(1, 'a'), (2, 'b'), (3, 'c')])
    assert isinstance(c, PairedCollection)
    assert c.to_dict() == {1: 'a', 2: 'b', 3: 'c'}


def test_paired_seq_2():
    c = paired_seq({1: 'a', 2: 'b', 3: 'c'})
    assert isinstance(c, PairedCollection)
    assert c.to_list() == [(1, 'a'), (2, 'b'), (3, 'c')]


def test_paired_append():
    c = seq(range(3))
    c = c.map_to_pair(identity, str)
    c = c.append((3, '3'))
    assert c.to_list() == [(0, '0'), (1, '1'), (2, '2'), (3, '3')]


def test_paired_conj():
    c = seq(range(3))
    c = c.map_to_pair(identity, str)
    c = c.conj((3, '3'))
    assert c.to_list() == [(0, '0'), (1, '1'), (2, '2'), (3, '3')]


def test_paired_cons():
    c = seq(range(3))
    c = c.map_to_pair(identity, str)
    c = c.cons((3, '3'))
    assert c.to_list() == [(3, '3'), (0, '0'), (1, '1'), (2, '2')]