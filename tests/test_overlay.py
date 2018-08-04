def test_overlay_get_radius(overlay):
    """
	Test that the size of theradius.
	"""
    expected = overlay.radius
    actual = 56

    assert expected == actual
