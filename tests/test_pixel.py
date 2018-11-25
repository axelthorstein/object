from pytest import raises

from object.pixel import PixelException


def test_pixel_color_property(pixel):
    """
    Test that only the most recent color is returned from the color property.
    """
    expected = 'grey'
    actual = pixel.color

    assert expected == actual


def test_pixel_color_is_not_out_of_bounds(pixel):
    """
    Test that valid coordinates return that it's in bounds.
    """
    expected = False
    actual = pixel.out_of_bounds((15, 15))

    assert expected == actual


def test_pixel_color_is_out_of_bounds(pixel):
    """
    Test that valid coordinates return that it is out of bounds.
    """
    with raises(PixelException):
        pixel.get_color((1, -1))
