from utils.color_utils import get_color, get_most_likely_colors


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
