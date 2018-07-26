def test_overlay_get_inner_radius(overlay):
    """
	Test that the inner radius is 27% of the total width.
	"""
    expected = overlay.inner_radius
    actual = 100 * 0.27

    assert expected == actual


def test_overlay_get_outer_radius(overlay):
    """
	Test that the outer radius is 27% of the total width.
	"""
    expected = overlay.outer_radius
    actual = 100 * 0.45

    assert expected == actual


def test_overlay_outer_radius_larger_than_inner_radius(overlay):
    """
	Test that the outer radius is larger than the inner radius.
	"""
    assert overlay.outer_radius > overlay.inner_radius


def test_overlay_get_inner_edges(overlay):
    """
	Test that the inner edges are the inner radius away
	from the starting coordinates.
	"""
    start_coord = 100
    radius = overlay.inner_radius
    expected = list(overlay.inner_edges.values())
    actual = [(start_coord - radius, start_coord), (start_coord,
                                                    start_coord + radius),
              (start_coord + radius, start_coord), (start_coord,
                                                    start_coord - radius)]

    assert expected == actual


def test_overlay_get_outer_edges(overlay):
    """
	Test that the outer edges are the outer radius away
	from the starting coordinates.
	"""
    start_coord = 100
    radius = overlay.outer_radius
    expected = list(overlay.outer_edges.values())
    actual = [(start_coord - radius, start_coord), (start_coord,
                                                    start_coord + radius),
              (start_coord + radius, start_coord), (start_coord,
                                                    start_coord - radius)]

    assert expected == actual
