def test_get_center_color(ring, updated_color_freq, starting_coordinates):
    """
	Test that the the highest voted color from the inner color frequencies
	would be returned.
	"""
    ring.color_freq = updated_color_freq

    expected = "red"
    actual = ring.get_center_color()

    assert expected == actual


def test_get_ring_color(ring, updated_color_freq, starting_coordinates):
    """
	Test that the the highest voted color from the inner color frequencies
	would be returned.
	"""
    ring.color_freq = updated_color_freq

    expected = "black"
    actual = ring.get_ring_color()

    assert expected == actual


def test_get_inner_edges():
    """
	"""
    pass


def test_get_outer_edges():
    """
	"""
    pass


def test_get_average_radius():
    """
	"""
    pass


def test_update_center_coords():
    """
	"""
    pass


def test_is_valid():
    """
	"""
    pass
