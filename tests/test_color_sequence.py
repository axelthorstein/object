def test_color_sequence_sort_coordinates(color_sequence):
    """
    Test that the list of coordinates is sorted using the degree from the
    center point starting with the leftmost point.
    """
    coordinates = [(5, 4), (3, 0), (4, 5), (5, 2), (0, 2), (1, 4), (6, 3),
                   (2, 0), (2, 5), (3, 6), (0, 3), (4, 1), (1, 1)]
    expected = [(0, 3), (1, 4), (2, 5), (3, 6), (4, 5), (5, 4), (6, 3), (5, 2),
                (4, 1), (3, 0), (2, 0), (1, 1), (0, 2)]
    actual = color_sequence.sort_coordinates(coordinates)

    assert expected == actual


def test_color_sequence_get_points_on_circumference(color_sequence):
    """
    Test that the list of coordinates are returned that form a circle around
    the center point.
    """
    expected = [(0, 3), (0, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 4), (6, 3),
                (5, 2), (5, 1), (3, 0), (1, 0), (0, 1)]
    actual = color_sequence.get_points_on_circumference()

    assert expected == actual


def test_color_sequence_get_points_on_circumference_upper_bound(
        color_sequence_high_grain, color_sequence_super_high_grain):
    """
    Test that there is an upper bound to the number of points to check on the
    circle.
    """
    expected = [(0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
                (5, 4), (6, 3), (5, 3), (5, 2), (5, 1), (5, 0), (4, 0), (3, 0),
                (2, 0), (1, 0), (0, 0), (0, 1), (0, 2)]
    high_grain = color_sequence_high_grain.get_points_on_circumference()
    highest_grain = color_sequence_super_high_grain.get_points_on_circumference(
    )

    assert high_grain == highest_grain == expected
