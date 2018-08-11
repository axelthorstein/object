def test_edge_scan_adjacent_pixel(edge, pixel):
    """
    Test that the pixel that is returned is the same color as the center pixel
    so that is increments on tne first direction it searches.
    """
    expected_color = 'grey'
    expected_coords = (30, 29)

    actual_pixel = edge.scan_adjacent_pixel(pixel, ['grey'])

    assert (expected_color == actual_pixel.color and
            expected_coords == actual_pixel.coords)


def test_edge_scan_adjacent_pixel_other_direction(edge, pixel):
    """
    Test that the pixel that is returned is the same color as the center pixel
    so that is increments on tne second direction it searches.
    """
    pixel.get_color(pixel.coords)
    expected_color = 'black'
    expected_coords = (30, 31)

    actual_pixel = edge.scan_adjacent_pixel(pixel, ['black'])

    assert (expected_color == actual_pixel.color and
            expected_coords == actual_pixel.coords)


def test_edge_scan_adjacent_pixel_original_direction(edge, pixel):
    """
    Test that the pixel that is returned is the same color as the center pixel
    so that is increments on tne second direction it searches.
    """
    expected_color = 'grey'
    expected_coords = (30, 30)

    actual_pixel = edge.scan_adjacent_pixel(pixel, ['blue'])

    assert (expected_color == actual_pixel.color and
            expected_coords == actual_pixel.coords)
