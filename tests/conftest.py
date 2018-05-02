import pytest

from o.overlay import Overlay


@pytest.fixture()
def starting_coordinates():
	return (10, 10)


@pytest.fixture()
def color_freq():
	return {"inner": {},"outer": {}}


@pytest.fixture()
def overlay():
	return Overlay((100, 100))
