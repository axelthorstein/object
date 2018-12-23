from object.detector import Detector
from object.image import Image
from object.product import Product

BASE_TEST_IMAGE_PATH = "/Users/axelthor/Projects/object/tests/test_images"


def get_sequence(image_name):
    """Return a sequence from the image name shorthand.
    """
    image = Image(f"{BASE_TEST_IMAGE_PATH}/{image_name}")
    detector = Detector(image, debug=True)

    return detector.get_sequence()


def test_detect_circle_black_and_white():
    sequence = get_sequence("circle_black_and_white.png")
    assert Product(sequence.color_code).is_valid()


def test_detect_circle_white_and_black():
    sequence = get_sequence("circle_white_and_black.png")
    assert Product(sequence.color_code).is_valid()


def test_detect_circle_med_36_square():
    sequence = get_sequence("circle_med_36_square.png")

    assert Product(sequence.color_code).is_valid()


def test_detect_circle_med_18_square():
    sequence = get_sequence("circle_med_18_square.png")
    assert Product(sequence.color_code).is_valid()


def test_detect_circle_thick_18_square():
    sequence = get_sequence("circle_thick_18_square.png")

    assert Product(sequence.color_code).is_valid()


def test_detect_circle_thin_18_square():
    sequence = get_sequence("circle_thin_18_square.png")

    assert Product(sequence.color_code).is_valid()


# Off Center Rings:

# def test_detect_circle_thick_18_round():
#     sequence = get_sequence("circle_thick_18_round.png")
#     assert Product(sequence.color_code).is_valid()

# def test_detect_circle_med_18_round():
#     sequence = get_sequence("circle_med_18_round.png")
#     assert Product(sequence.color_code).is_valid()

# def test_detect_circle_thin_18_round():
#     sequence = get_sequence("circle_thin_18_round.png")
#     assert Product(sequence.color_code).is_valid()

# def test_detect_circle_med_36_round():
#     sequence = get_sequence("circle_med_36_round.png")
#     assert Product(sequence.color_code).is_valid()

# def test_detect_circle_thin_50_square():
#     # Can't apply the filters because the dashes are too thin.
#     image_path = f"{BASE_TEST_IMAGE_PATH}/circle_thin_50_square.png"
#     detect = Detector(image_path, apply_filters=False)
#     ring = detect.detect()

#     assert Product(sequence.color_code).is_valid()

# Real world tests:

# def test_detect_real_test_circle_1():
#     sequence = get_sequence("real_test_circle_1.png")
#     assert Product(sequence.color_code).is_valid()

# def test_detect_real_test_circle_2():
#     sequence = get_sequence("real_test_circle_2.png")
#     assert Product(sequence.color_code).is_valid()

# def test_detect_real_test_circle_3():
#     image_path = f"{BASE_TEST_IMAGE_PATH}/real_test_circle_3.png"
#     detect = Detector(image_path, merge_filter=True)
#     ring = detect.detect()

#     assert Product(sequence.color_code).is_valid()

# def test_detect_real_test_circle_4():
#     image_path = f"{BASE_TEST_IMAGE_PATH}/real_test_circle_4.png"
#     detect = Detector(image_path, merge_filter=True)
#     ring = detect.detect()

#     assert Product(sequence.color_code).is_valid()

# def test_detect_real_test_circle_5():
#     sequence = get_sequence("real_test_circle_5.png")
#     assert Product(sequence.color_code).is_valid()

# def test_detect_circle_thick_18_square_sim_colors():
#     sequence = get_sequence("circle_thick_18_square_sim_colors.png")
#     from pprint import pprint
#     pprint(ring.sequence.sequence)
#     exit()
#     assert Product(sequence.color_code).is_valid()

# def test_detect_circle_peach_merged():
#     sequence = get_sequence("peach_merged.png")
#     from pprint import pprint
#     pprint(ring.sequence.sequence)
#     exit()
#     assert Product(sequence.color_code).is_valid()
