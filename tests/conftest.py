import pytest
from unittest.mock import Mock
from collections import Counter

from obj.dashed_ring import Dashed
from obj.coordinate import Coordinate
from obj.overlay import Overlay


@pytest.fixture()
def starting_coordinates():
    """
	Starting coordinates on a pixel matrix.
	"""
    return (10, 10)


@pytest.fixture()
def depths():
    """
	The inner and outer depths.
	"""
    return ["inner", "outer"]


@pytest.fixture()
def overlay(image):
    """
	An overlay instantiated with the center coordinates at (100, 100).
	"""
    return Overlay(image, (100, 100))


@pytest.fixture()
def image():
    """
	A mock for the image.
	"""
    image = Mock()
    image.getpixel.return_value = (100, 100, 100)

    return image


@pytest.fixture()
def ring(image, starting_coordinates):
    """
	A Ring.
	"""
    ring = Dashed(image, starting_coordinates)
    return ring


@pytest.fixture()
def inner_coordinate(image, depths):
    """
	An inner coordinate.
	"""
    coordinate = Coordinate(image, depths[0])

    return coordinate


@pytest.fixture()
def outer_coordinate(image, depths):
    """
	An outer coordinate.
	"""
    coordinate = Coordinate(image, depths[1])

    return coordinate
