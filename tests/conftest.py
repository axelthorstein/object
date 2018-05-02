import pytest


@pytest.fixture()
def starting_coordinates():
	return (10, 10)


@pytest.fixture()
def color_freq():
	return {"inner": {},"outer": {}}
