from o.detect import Detect, DetectionStrategy


def test_detect():
    """
    Run the full detect ring method with a real image. Run with debug so the
    ring dimensions are outputted and the coordinates are drawn on the image.
    """
    Detect("/Users/axelthor/Projects/object/images/small_ring.png",
        strategy=DetectionStrategy.SIMPLE, debug=True).detect_ring()