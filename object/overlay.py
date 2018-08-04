class Overlay:
    """
    An object to represent the overlay over the camera.
    """

    def __init__(self, center_point):
        self.center_point = center_point
        self.radius = self.get_radius()

    def get_radius(self):
        """Find the radius of the middle of the outer circle.

        Returns:
            int: The average radius.
        """
        inner_radius = int(self.center_point.y * 0.45)
        outer_radius = int(self.center_point.y * 0.22)

        return int(inner_radius + (outer_radius / 2))

    def __str__(self):
        """Return a description of the overlay.

        Returns:
            str: The string representation of the overlay.
        """
        return f'Overlay {self.center_point} with {self.radius} radius.'

    def __repr__(self):
        desc = f'\n{self.__class__.__name__}:\n'

        for attribute in self.__dict__:
            key = attribute.replace('_', ' ').capitalize()
            desc += f'    {key}: {self.__dict__[attribute]},\n'

        return desc
