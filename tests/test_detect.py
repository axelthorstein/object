from obj.detect import Detect, DetectionStrategy

# def test_detect_simple_ring():
#     """
#     Run the full detect ring method with a real image. Run with debug so the
#     ring dimensions are outputted and the coordinates are drawn on the image.
#     """
#     Detect("/Users/axelthor/Projects/object/images/small_ring.png",
#     strategy=DetectionStrategy.SIMPLE, debug=True).detect_ring()


def get_dashed_ring(image_name):
    """Return a dashed ring from the image name shorthand.
    """
    detect = Detect(
        f"/Users/axelthor/Projects/object/images/{image_name}",
        strategy=DetectionStrategy.DASHED,
        debug=False)

    return detect.detect_ring()


def test_detect_circle_med_36_square():
    ring = get_dashed_ring("circle_med_36_square.png")

    assert ring.is_valid()


def test_detect_circle_med_36_round():
    ring = get_dashed_ring("circle_med_36_round.png")

    assert ring.is_valid()


def test_detect_circle_med_18_square():
    ring = get_dashed_ring("circle_med_18_square.png")

    assert ring.is_valid()


def test_detect_circle_med_18_round():
    ring = get_dashed_ring("circle_med_18_round.png")

    assert ring.is_valid()


def test_detect_circle_thick_18_square():
    ring = get_dashed_ring("circle_thick_18_square.png")

    assert ring.is_valid()


def test_detect_circle_thick_18_round():
    ring = get_dashed_ring("circle_thick_18_round.png")

    assert ring.is_valid()


# def test_detect_circle_thin_18_square():
#     ring = get_dashed_ring("circle_thin_18_square.png")

#     assert ring.is_valid()

# def test_detect_circle_thin_18_round():
#     ring = get_dashed_ring("circle_thin_18_round.png")

#     assert ring.is_valid()
