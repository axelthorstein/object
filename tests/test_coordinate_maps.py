def test_coordinate_maps_sort_coordinates(coordinate_map):
    """
    Test that the list of coordinates is sorted using the degree from the
    center point starting with the leftmost point.
    """
    coordinates = [(5, 4), (3, 0), (4, 5), (5, 2), (0, 2), (1, 4), (6, 3),
                   (2, 0), (2, 5), (3, 6), (0, 3), (4, 1), (1, 1)]
    expected = [(0, 3), (1, 4), (2, 5), (3, 6), (4, 5), (5, 4), (6, 3), (5, 2),
                (4, 1), (3, 0), (2, 0), (1, 1), (0, 2)]
    actual = coordinate_map.sort_coordinates(coordinates)

    assert expected == actual


def test_coordinate_map_get_coordinates(coordinate_map):
    """
    Test that the list of coordinates are returned that form a circle around
    the center point.
    """
    expected = [(0, 3), (0, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 4), (6, 3),
                (5, 2), (5, 1), (3, 0), (1, 0), (0, 1)]
    actual = coordinate_map.get_coordinates()

    assert expected == actual


def test_coordinate_map_get_coordinates_upper_bound(
        coordinate_map_high_grain, coordinate_map_super_high_grain):
    """
    Test that there is an upper bound to the number of points to check on the
    circle.
    """
    expected = [(0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
                (5, 4), (6, 3), (5, 3), (5, 2), (5, 1), (5, 0), (4, 0), (3, 0),
                (2, 0), (1, 0), (0, 0), (0, 1), (0, 2)]
    high_grain = coordinate_map_high_grain.get_coordinates()
    highest_grain = coordinate_map_super_high_grain.get_coordinates()

    assert high_grain == highest_grain == expected
