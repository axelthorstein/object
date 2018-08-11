def test_overlay_get_radius(overlay):
    """
	Test the size of the radius.
	"""
    expected = overlay.radius
    actual = 56

    assert expected == actual
