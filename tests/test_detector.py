from obj.detector import Detector


def get_ring(image_name):
    """Return a dashed ring from the image name shorthand.
    """
    detector = Detector(
        f"/Users/axelthor/Projects/object/tests/test_images/{image_name}",
        debug=False)

    return detector.detect()


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
    detect = Detecto(
        f"/Users/axelthor/Projects/object/tests/test_images/circle_thin_50_square.png",
        debug=False)
    ring = detect.detect(grain=3600)
    assert ring.is_valid()
