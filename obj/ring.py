class Ring(object):
    """
    An abstract Ring object.
    """

    @staticmethod
    def format_edges(edges):
        """Return a string representation of the overlays edges.

        Returns:
            str: The overlay edges.
        """
        return "".join([
            "\n"
            "    Left coordinates:  {}\n".format(edges["left"]),
            "    Up coordinates:    {}\n".format(edges["up"]),
            "    Right coordinates: {}\n".format(edges["right"]),
            "    Down coordinates:  {}".format(edges["down"])
        ])


class RingException(Exception):
    pass
