from pytest import raises

from utils.color_utils import get_color
from utils.color_utils import get_most_likely_colors
from utils.color_utils import sequence_to_color_code
from utils.color_utils import get_hue_name
from utils.color_utils import ColorException


def test_get_color_name_returns_three_colors():
    """
	Test that the method returns a set of three likely colors.
	"""
    expected = ['black', 'darkgreen', 'midnightblue']
    actual = get_most_likely_colors((0, 0, 0))

    assert expected == actual


def test_get_color_name_returns_a_color():
    """
    Test that the method returns a color.
    """
    expected = ["green"]
    actual = get_color((81, 255, 152))

    assert expected == actual


def test_get_color_name_returns_black():
    """
    Test that the method returns black.
    """
    expected = ["black"]
    actual = get_color((0, 0, 0))

    assert expected == actual


def test_get_color_name_returns_white():
    """
    Test that the method returns white.
    """
    expected = ["white"]
    actual = get_color((255, 255, 255))

    assert expected == actual


def test_get_color_name_light_red_returns_red():
    """
    Test that very light red doesn't return white.
    """
    expected = ["red"]
    actual = get_color((255, 230, 230))

    assert expected == actual


def test_get_color_name_super_light_red_returns_white():
    """
    Test that super light red returns white.
    """
    expected = ["white"]
    actual = get_color((255, 235, 235))

    assert expected == actual


def test_get_color_name_mostly_dark_red_returns_black():
    """
    Test that mostly dark red returns black.
    """
    expected = ["red"]
    actual = get_color((55, 0, 0))

    assert expected == actual


def test_get_color_name_super_dark_red_returns_black():
    """
    Test that super dark red returns black.
    """
    expected = ["black"]
    actual = get_color((50, 0, 0))

    assert expected == actual


def test_get_color_name_low_bightness_returns_grey():
    """
    Test that low brightness returns grey.
    """
    expected = ["grey"]
    actual = get_color((99, 75, 75))

    assert expected == actual


def test_get_color_name_high_bightness_returns_grey():
    """
    Test that high brightness returns grey.
    """
    expected = ["grey"]
    actual = get_color((199, 175, 175))

    assert expected == actual


def test_get_color_name_all_colors_return_grey():
    """
    Test that all given colors return grey.
    """
    colors = [(112, 100, 100), (199, 175, 175), (186, 174, 174), (81, 75, 75)]
    actual = set()
    expected = {"grey"}

    for color in colors:
        actual.add(get_color(color)[0])

    assert expected == actual


def test_sequence_to_color_code():
    """
    Test that a sequence returns a valid code.
    """
    sequence = ['green', 'green', 'green', 'red', 'red', 'red', 'blue', 'blue']
    expected = '0303030000000404'
    actual = sequence_to_color_code(sequence)

    assert expected == actual


def test_sequence_to_color_code_raises_exception_on_invalid_color_name():
    """
    Test that an exception is raised when passed an invalid color name.
    """
    sequence = ['maroon', 'green', 'green', 'red', 'red', 'red', 'blue', 'blue']

    with raises(ColorException, match="Color maroon not found."):
        sequence_to_color_code(sequence)


def test_sequence_to_color_code_with_empty_sequence():
    """
    Test that a sequence returns an empty string when it intakes a empty
    sequence.
    """
    sequence = []
    expected = ''
    actual = sequence_to_color_code(sequence)

    assert expected == actual


def test_get_hue_name():
    """
    Test that the correct hue name is returned.
    """
    expected = 'red'
    actual = get_hue_name(0)

    assert expected == actual


def test_get_hue_name_raises_exception_on_invalid_hue():
    """
    Test that an exception is raised when passed an invalid hue value.
    """
    with raises(ColorException, match="Hue -1 not found."):
        get_hue_name(-1)
