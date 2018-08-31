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
    pixel.update_coords(15, 16)

    expected_x = 15
    expected_y = 16
    expected_coords = (15, 16)

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
    pixel.update_coords(15, 15)
    actual = pixel.out_of_bounds()

    assert expected == actual


def test_pixel_color_is_out_of_bounds(pixel):
    """
    Test that valid coordinates return that it is out of bounds.
    """
    with raises(PixelException):
        pixel.update_coords(1, -1)


def test_pixel_scan_adjacent_pixels(pixel):
    """
    Test that the pixel that is returned is the same color as the center pixel
    so that is increments on tne first direction it searches.
    """
    expected_color = 'grey'
    expected_coords = (30, 29)

    pixel.scan_adjacent_pixels(Direction.left, ['grey'])

    assert (expected_color == pixel.color and expected_coords == pixel.coords)


def test_pixel_scan_adjacent_pixels_other_direction(pixel):
    """
    Test that the pixel that is returned is the same color as the center pixel
    so that is increments on tne second direction it searches.
    """
    pixel.get_color(pixel.coords)
    expected_color = 'black'
    expected_coords = (30, 31)

    pixel.scan_adjacent_pixels(Direction.left, ['black'])

    assert (expected_color == pixel.color and expected_coords == pixel.coords)


def test_pixel_scan_adjacent_pixels_original_direction(pixel):
    """
    Test that if the expected color isn't seen then the original pixel will get
    returned.
    """
    expected_color = 'grey'
    expected_coords = (30, 30)

    pixel.scan_adjacent_pixels(Direction.left, ['blue'])

    assert (expected_color == pixel.color and expected_coords == pixel.coords)