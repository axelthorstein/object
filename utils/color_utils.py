import webcolors
from operator import itemgetter


class ColorException(Exception):
    pass        


def get_color(rgb):
    """Get the name of a color for a RGB value.

    Resolve the three closest human readable names for a RBG value.

    Args:
        rgb (list of int): The Red, Green, Blue triplet.

    Returns:
        set of str: The closest color names from the RGB value.
    """
    min_colors = {}

    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb[0]) ** 2
        gd = (g_c - rgb[1]) ** 2
        bd = (b_c - rgb[2]) ** 2
        min_colors[(rd + gd + bd)] = name

    # Sort the keys based on the minimum values, indicating liklihood.
    min_colors = [min_colors[key] for key in sorted(
        min_colors.keys(), reverse=False)]

    # Return the 3 most likely colors in order of likelihood.
    return set(min_colors[:3])


def update_color_freq(color_freq, current_colors, depth):
    """Update the color local freq Counter.

    Track the frequency of a color for the given depth and direction, and
    multiply it by the likelihood that the correct color was identified.
    
    Args:
        color_freq (Counter): The freq of colors.
        current_colors (tuple): The next pixel's color.
        depth (str): Whether this is for inner or outer colours.

    Returns:
        color_freq (Counter): The freq of colors.
    """
    for i, color in enumerate(reversed(list(current_colors))):
        if color in color_freq[depth].keys():
            color_freq[depth][color] += 1 * i
        else:
            color_freq[depth][color] = 1 * i

    return color_freq
