from math import atan2, cos, degrees, sin
from operator import sub

from object.coordinate_maps.coordinate_map import CoordinateMap


class DashedRingMap(CoordinateMap):
    """A coordinate map for sampling the coordinates from a dashed ring."""

    def __init__(self, center_point, radius, grain):
        super(DashedRingMap, self).__init__()
        self.center_point = center_point
        self.radius = radius
        self.grain = grain
        self.coordinates = self.get_coordinates()

    def sort_coordinates(self, coordinates):
        """Sort the coordinates counter clockwise around the center.

        The coordinates need to be sorted so that they are in order of how they
        appear arround the center so that we can get an accurate ordering of
        colors in the dashes.

        Implementation from Stack Overflow commnent:
        https://stackoverflow.com/questions/51074984/
        sorting-according-to-clockwise-point-coordinates/51075419

        "On second thought that actually won't work, since for every coordinate
        on the list there's always another coordinate whose vector to the
        centroid is clockwise to that of the said coordinate, so there will be
        no "bottom" to the comparison. In OP's case, we need -135 degrees to be
        the "bottom" of the sorted list of coordinates. The sign of the 2D
        cross-product can only help determine if one vector is clockwise to
        another but cannot help establish how far away from the "bottom"
        (i.e. -135 degrees) a vector is."

        Args:
            coordinates (List[Tuple[int, int]]): The ring coordinates.

        Returns:
            List[Tuple[int, int]]: The sorted coordinates.
        """
        leftmost_degree = 180
        return sorted(coordinates, key=lambda coord: (leftmost_degree - degrees(
            atan2(*tuple(map(sub, coord, self.center_point.coords))[::-1]))) % 360)

    def get_coordinates(self):
        """Find all the coordinates on the circumference on the ring.

        Increasing the grain will potentially increase accuracy, but will be
        negligable beyond a certain point and will also increase runtime.

        Returns:
            List[Tuple[int, int]]: The sorted coordinates.
        """
        coordinates = []

        for point in range(self.grain):
            x = int(self.radius * cos(point) + self.center_point.x)
            y = int(self.radius * sin(point) + self.center_point.y)

            coordinates.append((x, y))

        coordinates = CoordinateMap.deduplicate(coordinates)

        sorted_coordinates = self.sort_coordinates(coordinates)

        return sorted_coordinates
