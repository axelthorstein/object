import pytest
from collections import Counter

from o.overlay import Overlay
from utils.color_utils import update_color_freq


@pytest.fixture()
def starting_coordinates():
	return (10, 10)


@pytest.fixture()
def color_freq():
	return {"inner": Counter(),"outer": Counter()}


@pytest.fixture()
def updated_color_freq(color_freq):
	current_colors = ("red", "black", "blue")
	for i in range(3):
		color_freq = update_color_freq(color_freq, current_colors, depth="inner")

	current_colors = ("black", "blue", "red")
	for i in range(3):
		color_freq = update_color_freq(color_freq, current_colors, depth="outer")

	return color_freq


@pytest.fixture()
def overlay():
	return Overlay((100, 100))
