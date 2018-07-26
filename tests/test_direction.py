import pytest

from obj.direction import Direction, DirectionException


def test_direction_left(starting_coordinates):
    """Test that the x coordinate is decremented by 1.
	"""
    assert Direction.left(starting_coordinates) == (9, 10)


def test_direction_up(starting_coordinates):
    """Test that the y coordinate is incremented by 1.
	"""
    assert Direction.up(starting_coordinates) == (10, 9)


def test_direction_right(starting_coordinates):
    """Test that the x coordinate is incremented by 1.
	"""
    assert Direction.right(starting_coordinates) == (11, 10)


def test_direction_down(starting_coordinates):
    """Test that the y coordinate is decremented by 1.
	"""
    assert Direction.down(starting_coordinates) == (10, 11)


def test_direction_left_and_up(starting_coordinates):
    """Test that the x and y coordinate is decremented by 1.
	"""
    assert Direction.left_and_up(starting_coordinates) == (9, 9)


def test_direction_right_and_up(starting_coordinates):
    """Test that the x and y coordinate is incremented by 1.
	"""
    assert Direction.right_and_up(starting_coordinates) == (11, 9)


def test_direction_right_and_down(starting_coordinates):
    """Test that the x and y coordinate is incremented by 1.
	"""
    assert Direction.right_and_down(starting_coordinates) == (11, 11)


def test_direction_left_and_down(starting_coordinates):
    """Test that the x and y coordinate is decremented by 1.
	"""
    assert Direction.left_and_down(starting_coordinates) == (9, 11)


def test_direction_left_five(starting_coordinates):
    """Test that the x coordinate is decremented by 5.
	"""
    assert Direction.left(starting_coordinates, steps=5) == (5, 10)


def test_direction_left_raises_error_on_negative_coord(starting_coordinates):
    """Test that the coordinate will raise an exception
	it tries to direction to a negative coordinate.
	"""

    with pytest.raises(DirectionException):
        Direction.left(starting_coordinates, steps=11)


def test_direction_down_raises_error_on_negative_coord(starting_coordinates):
    """Test that the coordinate will raise an exception
	it tries to direction to a negative coordinate.
	"""
    with pytest.raises(DirectionException):
        Direction.left(starting_coordinates, steps=11)
