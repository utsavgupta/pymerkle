import sys
sys.path.append("../")

import pytest
import src.merkle

def test_hash_identity(mtree):
    assert(mtree._h("test") == "test")

def test_inclusion_of_lines(mtree, test_data):
    for linum, line in enumerate(test_data):
        assert(str(linum) + line in mtree._hashes)

def test_leaf_position(mtree, test_data):
    for linum, line in enumerate(test_data):
        assert(mtree._index[str(linum) + line] == linum)

def test_root_hash(mtree, test_data):
    expected_hashes = [str(linum) + line for linum, line in enumerate(test_data)]
    expected_root = reduce(lambda x, y: x + y, expected_hashes)

    assert(mtree.root_hash() == expected_root)

def test_merkle_path(mtree):

    # test merkle path for a
    expected_path = ['11b', '12c3d', '14e5f6g7h']
    assert(mtree.merkle_path('0a') == expected_path)

    # test merkle path for b
    expected_path = ['00a', '12c3d', '14e5f6g7h']
    assert(mtree.merkle_path('1b') == expected_path)

    # test merkle path for c
    expected_path = ['13d', '00a1b', '14e5f6g7h']
    assert(mtree.merkle_path('2c') == expected_path)

    # test merkle path for d
    expected_path = ['02c', '00a1b', '14e5f6g7h']
    assert(mtree.merkle_path('3d') == expected_path)
    
    # test merkle path for e
    expected_path = ['15f', '16g7h', '00a1b2c3d']
    assert(mtree.merkle_path('4e') == expected_path)

    # test merkle path for f
    expected_path = ['04e', '16g7h', '00a1b2c3d']
    assert(mtree.merkle_path('5f') == expected_path)

    # test merkle path for g
    expected_path = ['17h', '04e5f', '00a1b2c3d']
    assert(mtree.merkle_path('6g') == expected_path)

    # test merkle path for h
    expected_path = ['06g', '04e5f', '00a1b2c3d']
    assert(mtree.merkle_path('7h') == expected_path)
