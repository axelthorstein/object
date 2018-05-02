import pytest

from o.move import Move, CoordinateException

def test_move_left(starting_coordinates):
	"""Test that the x coordinate is decremented by 1.
	"""
	assert Move.left(starting_coordinates) == (9, 10)


def test_move_up(starting_coordinates):
	"""Test that the y coordinate is incremented by 1.
	"""
	assert Move.up(starting_coordinates) == (10, 11)


def test_move_right(starting_coordinates):
	"""Test that the x coordinate is incremented by 1.
	"""
	assert Move.right(starting_coordinates) == (11, 10)


def test_move_down(starting_coordinates):
	"""Test that the y coordinate is decremented by 1.
	"""
	assert Move.down(starting_coordinates) == (10, 9)


def test_move_left_five(starting_coordinates):
	"""Test that the x coordinate is decremented by 5.
	"""
	assert Move.left(starting_coordinates, jump=5) == (5, 10)


def test_move_left_raises_error_on_negative_coord(starting_coordinates):
	"""Test that the coordinate will raise an exception
	it tries to move to a negative coordinate.
	"""

	with pytest.raises(CoordinateException):
		Move.left(starting_coordinates, jump=11)


def test_move_down_raises_error_on_negative_coord(starting_coordinates):
	"""Test that the coordinate will raise an exception
	it tries to move to a negative coordinate.
	"""
	with pytest.raises(CoordinateException):
		Move.left(starting_coordinates, jump=11)
