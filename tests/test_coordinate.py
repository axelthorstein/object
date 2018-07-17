

def test_get_pixel(inner_coordinate, starting_coordinates):
	"""
	Test retriving the pixel from the coordinate. This is depth independent
	so we don't need to test with different depths.
	"""
	expected = {'grey'}
	actual = inner_coordinate.get_pixel_colors(starting_coordinates)

	assert expected == actual


def test_get_inner_edges():
	"""
	"""
	pass


def test_get_inner_edges():
	"""
	"""
	pass
