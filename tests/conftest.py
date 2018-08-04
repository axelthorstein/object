from unittest.mock import Mock
from pytest import fixture

from obj.ring import Ring
from obj.coordinate import Coordinate
from obj.overlay import Overlay
from obj.pixel import Pixel


@fixture()
def starting_coordinates():
    """
	Starting coordinates on a pixel matrix.
	"""
    return (10, 10)


@fixture()
def depths():
    """
	The inner and outer depths.
	"""
    return ["inner", "outer"]


@fixture()
def overlay(image):
    """
	An overlay instantiated with the center coordinates at (100, 100).
	"""
    center_pixel = Pixel(image, (100, 100))
    return Overlay(center_pixel)


@fixture()
def image():
    """
	A mock for the image.
	"""
    image = Mock()
    image.getpixel.return_value = (100, 100, 100)

    return image


@fixture()
def ring(image, starting_coordinates):
    """
	A Ring.
	"""
    ring = Ring(image, starting_coordinates)
    return ring


@fixture()
def inner_coordinate(image, depths):
    """
	An inner coordinate.
	"""
    coordinate = Coordinate(image, depths[0])

    return coordinate


@fixture()
def outer_coordinate(image, depths):
    """
	An outer coordinate.
	"""
    coordinate = Coordinate(image, depths[1])

    return coordinate
