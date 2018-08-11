from pytest import raises

from object.pixel import PixelException
from object.direction import Direction


def test_pixel_color_property(pixel):
    """
    Test that only the most recent color is returned from the color property.
    """
    expected = 'grey'
    actual = pixel.color

    assert expected == actual


def test_pixel_color_property_multiple_colors(pixel):
    """
    Test that only the most recent color is returned from the color property
    when there are multiple colors in the colors attribute.
    """
    pixel.move(Direction.left, 1)
    pixel.move(Direction.left, 1)
    pixel.move(Direction.left, 1)

    expected = 'black'
    actual = pixel.color

    assert expected == actual


def test_pixel_color_update_coords(pixel):
    """
    Test that only the most recent color is returned from the color property
    when there are multiple colors in the colors attribute.
    """
    old_coords = pixel.coords
    pixel.update_coords(20, 10)

    expected_x = 20
    expected_y = 10
    expected_coords = (20, 10)

    actual_x = pixel.x
    actual_y = pixel.y
    actual_coords = pixel.coords

    assert (expected_x == actual_x and expected_y == actual_y and
            expected_coords == actual_coords and old_coords != actual_coords)


def test_pixel_color_update_coords_raises_exception(pixel):
    """
    Test that an exception is raised if the pixel tries to move out of bounds.
    """
    with raises(PixelException):
        pixel.update_coords(-1, 2)


def test_pixel_color_colors_intersect(pixel):
    """
    Test that the colors are properly identified as intersecting.
    """
    expected = [False, False, True]
    actual = []
    pixel.move(Direction.left, 1)
    actual.append(pixel.colors_intersect(['black']))
    pixel.move(Direction.left, 1)
    actual.append(pixel.colors_intersect(['black']))
    pixel.move(Direction.left, 1)
    actual.append(pixel.colors_intersect(['black']))

    assert expected == actual


def test_pixel_color_is_not_out_of_bounds(pixel):
    """
    Test that valid coordinates return that it's in bounds.
    """
    expected = False
    pixel.update_coords(20, 10)
    actual = pixel.out_of_bounds()

    assert expected == actual


def test_pixel_color_is_out_of_bounds(pixel):
    """
    Test that valid coordinates return that it is out of bounds.
    """
    with raises(PixelException):
        pixel.update_coords(1, -1)
