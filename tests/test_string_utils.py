from utils.string_utils import are_rotations


def test_are_rotations():
    expected = True
    actual = are_rotations('abcd', 'bcda')

    assert expected == actual


def test_are_rotations_identical():
    expected = True
    actual = are_rotations('abcd', 'abcd')

    assert expected == actual


def test_are_not_rotations():
    expected = False
    actual = are_rotations('abcd', 'bcde')

    assert expected == actual


def test_are_not_rotations_different_lengths():
    expected = False
    actual = are_rotations('abcd', 'bcd')

    assert expected == actual


def test_are_not_rotations_invalid_order():
    expected = False
    actual = are_rotations('bacd', 'abcd')

    assert expected == actual
