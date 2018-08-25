from object.detector import Detector
from image_filters.rag_merge_filter import rag_merge_filter

def get_ring(image_name):
    """Return a dashed ring from the image name shorthand.
    """
    detector = Detector(
        f"/Users/axelthor/Projects/object/tests/test_images/{image_name}",
        debug=True)

    return detector.find_ring()


def test_detect_circle_med_36_square():
    ring = get_ring("circle_med_36_square.png")
    assert ring.is_valid()


def test_detect_circle_med_36_round():
    ring = get_ring("circle_med_36_round.png")
    assert ring.is_valid()


def test_detect_circle_med_18_square():
    ring = get_ring("circle_med_18_square.png")
    assert ring.is_valid()


def test_detect_circle_med_18_round():
    ring = get_ring("circle_med_18_round.png")
    assert ring.is_valid()


def test_detect_circle_thick_18_square():
    ring = get_ring("circle_thick_18_square.png")
    assert ring.is_valid()


def test_detect_circle_thick_18_round():
    ring = get_ring("circle_thick_18_round.png")
    assert ring.is_valid()


def test_detect_circle_thin_18_square():
    ring = get_ring("circle_thin_18_square.png")
    assert ring.is_valid()


def test_detect_circle_thin_18_round():
    ring = get_ring("circle_thin_18_round.png")

    assert ring.is_valid()


def test_detect_circle_thin_50_square():
    detect = Detector(
        f"/Users/axelthor/Projects/object/tests/test_images/circle_thin_50_square.png",
        debug=True)
    ring = detect.find_ring(grain=3600)
    assert ring.is_valid()


def test_detect_debug_image():
    image_path = 'tests/test_images/real_test_circle_rgb.png'
    out_path = 'images/debug.png'
    rag_merge_filter(image_path, out_path)

    detect = Detector(
        f"/Users/axelthor/Projects/object/images/debug.png", debug=True)
    ring = detect.find_ring(grain=360)
    assert ring.is_valid()
