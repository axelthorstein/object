import pytest

from utils.color_utils import get_color, update_color_freq


def test_get_color_name_returns_three_colors():
	"""
	Test that the method returns a set of three likely colors.
	"""
	colors = get_color((0, 0, 0))

	assert colors == {"midnightblue", "black", "darkgreen"}


def test_update_inner_color_freq(color_freq):
	"""
	Test that the color frequencies are updated properly.
	"""
	current_colors = ("black", "red", "blue")
	actual = update_color_freq(color_freq, current_colors, depth="inner")

	expected = {
		"inner": {'black': 2, 'blue': 0, 'red': 1},
		"outer": {}
		}

	assert expected == actual

def test_update_inner_color_freq_updated_twice(color_freq):
	"""
	Test that the color frequencies are updated properly when updated twice.
	"""
	current_colors = ("black", "red", "blue")
	color_freq = update_color_freq(color_freq, current_colors, depth="inner")
	actual = update_color_freq(color_freq, current_colors, depth="inner")

	expected = {
		"inner": {'black': 4, 'blue': 0, 'red': 2},
		"outer": {}
		}

	assert expected == actual


def test_update_inner_and_outer_color_freq(color_freq):
	"""
	Test that the color frequencies are updated properly for inner and outer.
	"""
	current_colors = ("black", "red", "blue")
	color_freq = update_color_freq(color_freq, current_colors, depth="inner")
	actual = update_color_freq(color_freq, current_colors, depth="outer")

	expected = {
		"inner": {'black': 4, 'blue': 0, 'red': 2},
		"outer": {'black': 4, 'blue': 0, 'red': 2}
		}

	assert expected == actual


def test_update_inner_and_outer_color_freq(color_freq):
	"""
	Test that the color frequencies are updated in order.
	"""
	current_colors = ("red", "black", "blue")
	color_freq = update_color_freq(color_freq, current_colors, depth="inner")
	current_colors = ("blue", "red", "black")
	actual = update_color_freq(color_freq, current_colors, depth="inner")

	expected = {
		"inner": {'black': 1, 'blue': 2, 'red': 3},
		"outer": {}
		}

	assert expected == actual
