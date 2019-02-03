from unittest.mock import Mock
from unittest.mock import MagicMock
from pytest import fixture

from object.coordinate_maps.dashed_ring_map import DashedRingMap
from object.pixel import Pixel


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
def image():
    """
	A mock for the image.
	"""
    image = Mock()
    image.getpixel.return_value = (100, 100, 100)

    return image


@fixture()
def coordinate_map(center_pixel):
    """
    A coordinate map.
    """
    return DashedRingMap(center_pixel, 2.5)


@fixture()
def center_pixel(image):
    """
    Center pixel.
    """
    image.size = (150, 150)
    return Pixel(image, (3, 3))


@fixture()
def center_element():
    """
    The center color.
    """
    return '1'


@fixture()
def large_image():
    """
    A mock for a large image.
    """
    image = Mock()
    side_effect = [(100, 100, 100), (100, 100, 100), (100, 100, 100), (0, 0, 0),
                   (0, 0, 0), (255, 255, 255)]
    image.getpixel = MagicMock(side_effect=side_effect)
    image.size = (100, 100)

    return image


@fixture()
def pixel(large_image):
    """
    A pixel.
    """
    return Pixel(large_image, (30, 30))
