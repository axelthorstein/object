import cv2
import numpy as np

from obj.ring import Ring


class HoughTransform(Ring):
    """
    A ring object with a center point, and a distance radius to it's inner
    and outer rings.
    """

    def __init__(self, image, starting_coords, debug=True):
        self.image = image
        self.debug = debug
        self.ring_circles = self.get_ring_circles()
        self.inner_circle = self.ring_circles[0]
        self.outer_circle = self.ring_circles[1]
        self.center_coords = self.get_center_coords()
        self.inner_radius = self.get_inner_radius()
        self.outer_radius = self.get_outer_radius()
        self.ring_color = self.get_ring_color()
        self.center_color = self.get_center_color()
        self.is_valid = self.is_valid()

    def get_center_coords(self):
        """Find the center coordinates of the circle.

        Returns:
            int: The center coordinates.
        """
        return (self.inner_circle[0], self.inner_circle[1])

    def get_inner_radius(self):
        """Find the radius of the inner circle.

        Returns:
            int: The inner radius.
        """
        return self.inner_circle[2]

    def get_outer_radius(self):
        """Find the radius of the outer circle.

        Returns:
            int: The outer radius.
        """
        return self.outer_circle[2]

    def get_greyscale_image(image):
        """Convert the image to greyscale.

        Returns:
            np.array of array: The image matrix of pixels.
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def is_valid(self):
        """Determine if the ring is valid.
        
        TODO: Add real validity check.

        Returns:
            bool: Whether the ring is valid.
        """
        return (self.outer_circle[2] - self.inner_circle[2]) > 2

    def get_ring_circles(self):
        """Use the Hough Transform algorithm to find circles in the image.

        Returns:
            bool: Whether the ring is valid.
        """
        def round(nums, precision=0):
            return np.uint16(np.around(nums, precision))

        greyscale_image = HoughTransform.get_greyscale_image(self.image)

        c1 = round(cv2.HoughCircles(
            greyscale_image, cv2.HOUGH_GRADIENT, .5, 10, 10, 10, 10, 10)[0][0]
        )
        c2 = round(cv2.HoughCircles(
            greyscale_image, cv2.HOUGH_GRADIENT, 1.5, 10, 10, 10, 10, 10)[0][0]
        )

        if c1[2] > c2[2]:
            outer_circle = c1
            inner_circle = c2
        else:
            outer_circle = c2
            inner_circle = c1

        if round(inner_circle[0:1], -1) == round(outer_circle[0:1], -1):
            return inner_circle, outer_circle
        raise RingException("The circles have different center coordinates.")

    def __str__(self):
        """Return a string representation of the ring.

        Returns:
            str: The ring attributes.
        """
        return "".join(["\nRing:\n"
                "  Center coordinates: {}\n".format(self.center_coords),
                "  Inner circle: {}\n".format(self.inner_circle),
                "  Outer circle: {}\n".format(self.outer_circle),
                "  Inner radius: {}\n".format(self.inner_radius),
                "  Outer radius: {}\n".format(self.outer_radius),
                "  Center color: {}\n".format(self.center_color),
                "  Ring color:   {}\n".format(self.ring_color)
                ])
