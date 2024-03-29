from pytest import raises

from object.detector import Detector
from object.image import Image
from object.product import ProductException

BASE_TEST_IMAGE_PATH = "/Users/axelthor/Projects/object/tests/test_images"


def get_product(image_name):
    """Return a product from the image name shorthand.
    """
    image = Image(f"{BASE_TEST_IMAGE_PATH}/{image_name}")
    detector = Detector(image)

    return detector.detect_product()


# Known products:


def test_detect_circle_black_and_white():
    product = get_product("circle_black_and_white.png")

    assert product == 'circle-18-black-and-white'


def test_detect_circle_white_and_black():
    product = get_product("circle_white_and_black.png")

    assert product == 'circle-18-white-and-black'


def test_detect_circle_med_36_square():
    product = get_product("circle_med_36_square.png")

    assert product == 'circle-36-multi-color'


def test_detect_circle_med_18_square():
    product = get_product("circle_med_18_square.png")

    assert product == 'circle-18-multi-color'


def test_detect_circle_thick_18_square():
    product = get_product("circle_thick_18_square.png")

    assert product == 'circle-18-multi-color'


def test_detect_circle_thin_18_square():
    product = get_product("circle_thin_18_square.png")

    assert product == 'circle-18-multi-color'


def test_detect_circle_thick_18_square_all_colors():
    product = get_product("circle_thick_18_square_all_colors.png")

    assert product == 'circle-18-all-colors'


# Off center circles:


def test_detect_circle_thick_18_round():
    product = get_product("circle_thick_18_round.png")
    assert product == 'circle-18-multi-color'


def test_detect_circle_med_18_round():
    product = get_product("circle_med_18_round.png")
    assert product == 'circle-18-multi-color'


def test_detect_circle_thin_18_round():
    product = get_product("circle_thin_18_round.png")
    assert product == 'circle-18-multi-color'


def test_detect_circle_med_36_round():
    product = get_product("circle_med_36_round.png")
    assert product == 'circle-36-multi-color'


def test_detect_circle_thin_50_square():
    # Can't apply the filters because the dashes are too thin.
    image = Image(
        f"{BASE_TEST_IMAGE_PATH}/circle_thin_50_square.png",
        apply_filters=False)
    detector = Detector(image)

    return detector.detect_product() == 'circle-50-multi-color'


# Real world tests:


def test_detect_real_test_circle_1():
    product = get_product("real_test_circle_1.png")
    assert product == 'circle-18-multi-color'


def test_detect_real_test_circle_2():
    product = get_product("real_test_circle_2.png")
    assert product == 'circle-18-multi-color'


def test_detect_real_test_circle_3():
    image = Image(f"{BASE_TEST_IMAGE_PATH}/real_test_circle_3.png")
    detector = Detector(image)

    return detector.detect_product() == 'circle-18-multi-color'


def test_detect_real_test_circle_4():
    image = Image(
        f"{BASE_TEST_IMAGE_PATH}/real_test_circle_4.png", merge_filter=True)
    detector = Detector(image)

    return detector.detect_product() == 'circle-18-multi-color'


def test_detect_real_test_circle_5():
    product = get_product("real_test_circle_5.png")
    assert product == 'circle-18-multi-color'


def test_detect_circle_thick_18_square_sim_colors():
    product = get_product("circle_thick_18_square_sim_colors.png")
    assert product == 'circle-18-square-sim-colors'


# Unknown product tests:


def test_detect_circle_thick_18_square_random_colors():
    with raises(ProductException) as exception:
        get_product("circle_thick_18_square_random_colors.png")

    assert str(exception.value) == 'Product not found.'


def test_detect_circle_thick_18_square_one_off():
    with raises(ProductException) as exception:
        get_product("circle_thick_18_square_one_off.png")

    assert str(exception.value) == 'Product not found.'


def test_detect_circle_thick_18_square_pair_reversed():
    with raises(ProductException) as exception:
        get_product("circle_thick_18_square_pair_reversed.png")

    assert str(exception.value) == 'Product not found.'


def test_detect_circle_thick_18_square_three_reversed():
    with raises(ProductException) as exception:
        get_product("circle_thick_18_square_three_reversed.png")

    assert str(exception.value) == 'Product not found.'


def test_detect_circle_thick_18_square_one_removed():
    with raises(ProductException) as exception:
        get_product("circle_thick_18_square_one_removed.png")

    assert str(exception.value) == 'Product not found.'


def test_detect_circle_thick_18_square_two_removed():
    with raises(ProductException) as exception:
        get_product("circle_thick_18_square_two_removed.png")

    assert str(exception.value) == 'Product not found.'
