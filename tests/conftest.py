import pytest
from unittest.mock import Mock
from collections import Counter

from obj.coordinate import Coordinate
from obj.simple_ring import Simple
from obj.overlay import Overlay
from utils.color_utils import update_color_freq


@pytest.fixture()
def starting_coordinates():
    """
	Starting coordinates on a pixel matrix.
	"""
    return (10, 10)


@pytest.fixture()
def color_freq():
    """
	An empty color frequencies map for the inner and outer colors
	"""
    return {"inner": Counter(), "outer": Counter()}


@pytest.fixture()
def depths():
    """
	The inner and outer depths.
	"""
    return ["inner", "outer"]


@pytest.fixture()
def updated_color_freq(color_freq):
    """
	A color frequencies map for the inner and outer colors already populated
	with test data.
	"""
    current_colors = ("red", "black", "blue")
    for i in range(3):
        color_freq = update_color_freq(
            color_freq, current_colors, depth="inner")

    current_colors = ("black", "blue", "red")
    for i in range(3):
        color_freq = update_color_freq(
            color_freq, current_colors, depth="outer")

    return color_freq


@pytest.fixture()
def overlay():
    """
	An overlay instantiated with the center coordinates at (100, 100).
	"""
    return Overlay((100, 100))


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
    ring = Simple(image, starting_coordinates)
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
