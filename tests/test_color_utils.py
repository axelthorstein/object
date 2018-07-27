import pytest

from utils.color_utils import get_color, get_most_likely_colors, update_color_freq


def test_get_color_name_returns_three_colors():
    """
	Test that the method returns a set of three likely colors.
	"""
    colors = get_most_likely_colors((0, 0, 0))

    assert set(colors) == set(["midnightblue", "black", "darkgreen"])


def test_get_color_name_returns_a_color():
    """
    Test that the method returns a light color.
    """
    color = get_color((81, 255, 152))

    assert color == ["green"]


# def test_get_color_name_returns_a_light_color():
#     """
# 	Test that the method returns a light color.
# 	"""
#     color = get_color((81, 255, 152))

#     assert color == ["light-green"]

# def test_get_color_name_returns_a_dark_color():
#     """
# 	Test that the method returns a dark color.
# 	"""
#     color = get_color((0, 117, 46))

#     assert color == ["dark-green"]


def test_update_inner_color_freq(color_freq):
    """
	Test that the color frequencies are updated properly.
	"""
    current_colors = ("black", "red", "blue")
    actual = update_color_freq(color_freq, current_colors, depth="inner")

    expected = {"inner": {'black': 3, 'blue': 1, 'red': 2}, "outer": {}}

    assert expected == actual


def test_update_inner_color_freq_updated_twice(color_freq):
    """
	Test that the color frequencies are updated properly when updated twice.
	"""
    current_colors = ("black", "red", "blue")
    color_freq = update_color_freq(color_freq, current_colors, depth="inner")
    actual = update_color_freq(color_freq, current_colors, depth="inner")

    expected = {"inner": {'black': 6, 'blue': 2, 'red': 4}, "outer": {}}

    assert expected == actual


def test_update_inner_and_outer_color_freq(color_freq):
    """
	Test that the color frequencies are updated properly for inner and outer.
	"""
    current_colors = ("black", "red", "blue")
    color_freq = update_color_freq(color_freq, current_colors, depth="inner")
    actual = update_color_freq(color_freq, current_colors, depth="outer")

    expected = {
        "inner": {
            'black': 6,
            'blue': 2,
            'red': 4
        },
        "outer": {
            'black': 6,
            'blue': 2,
            'red': 4
        }
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

    expected = {"inner": {'black': 3, 'blue': 4, 'red': 5}, "outer": {}}

    assert expected == actual
