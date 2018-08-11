from unittest.mock import Mock
from unittest.mock import MagicMock
from pytest import fixture

from object.ring import Ring
from object.overlay import Overlay
from object.pixel import Pixel
from object.color_sequence import ColorSequence
from object.direction import Direction
from object.edge import Edge


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
    center_point = Pixel(image, (100, 100))
    return Overlay(center_point)


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
def color_sequence(image, center_pixel):
    """
    A color sequence.
    """
    return ColorSequence(image, center_pixel, 3, 16)


@fixture()
def color_sequence_high_grain(image, center_pixel):
    """
    A color sequence with a high grain.
    """
    return ColorSequence(image, center_pixel, 3, 360)


@fixture()
def color_sequence_super_high_grain(image, center_pixel):
    """
    A color sequence with a super high grain.
    """
    return ColorSequence(image, center_pixel, 3, 3600)


@fixture()
def center_pixel(image):
    """
    Center pixel.
    """
    return Pixel(image, (3, 3))


@fixture()
def center_element():
    """
    The center color.
    """
    return '1'


@fixture()
def directions():
    """
    A mapping of direction names to direction methods.
    """
    return Direction.get_directions()


@fixture()
def large_image():
    """
    A mock for a large image.
    """
    image = Mock()
    side_effect = [(100, 100, 100), (100, 100, 100), (100, 100, 100), (0, 0, 0),
                   (255, 255, 255)]
    image.getpixel = MagicMock(side_effect=side_effect)
    image.size = (100, 100)

    return image


@fixture()
def pixel(large_image):
    """
    A pixel.
    """
    return Pixel(large_image, (30, 30))


@fixture()
def edge(large_image):
    """
	An edge.
	"""
    return Edge(large_image, Direction.left, 'inner')
