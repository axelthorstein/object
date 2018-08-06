#pylint: disable=too-many-return-statements,too-many-branches
import colorsys
import webcolors

from configs.config import COLOR_RANGE_MAP
from configs.config import COLOR_CODE_MAP


class ColorException(Exception):
    pass


def sequence_to_code(sequence):
    """Create a deterministic code of fixed length from the color sequence.

    Args:
        sequence (List[str]): The sequence of color names.

    Returns:
        str: The color code sequence string.

    Raises:
        ColorException: If the color name doesn't have a corresponding code.
    """
    code = ''

    try:
        for color in sequence:
            code += COLOR_CODE_MAP[color]
    except KeyError:
        raise ColorException(f"Color {color} not found.")

    return code


def get_hue_name(hue):
    """Get the name of a hue.

    Args:
        hue (int): The value of a hue from a HSV tuple.

    Returns:
        str: The color name from the hue value.

    Raises:
        ColorException: If the hue isn't in any color range.
    """
    try:
        return COLOR_RANGE_MAP[hue]
    except KeyError:
        raise ColorException(f"Hue {hue} not found.")


def get_color(rgb):
    """Get the name of a color for a RGB value.

    Resolve the human readable names for a RBG value. This method is a great
    speed increase over the `get_most_likely_colors` method, however it assumes
    that the hue is the exact color name and is limited to 16 colors (for now).

    Args:
        rgb (List[int]): The Red, Green, Blue triplet.

    Returns:
        List[str]: The color name from the RGB value.
    """
    hsv = colorsys.rgb_to_hsv(*rgb[0:3])
    hue = int(hsv[0] * 360)
    saturation = hsv[1]
    brightness = hsv[2] / 255

    if brightness < 0.20:
        color = 'black'
    elif saturation < 0.09 and brightness > 0.91:
        color = 'white'
    elif (saturation < 0.25 and brightness < 0.40) or (saturation < 0.15 and
                                                       brightness < 0.80):
        color = 'grey'
    else:
        color = get_hue_name(hue)

    return [color]


def get_most_likely_colors(rgb):
    """Get the name of a color for a RGB value.

    Resolve the three closest human readable names for a RBG value.

    Args:
        rgb (List[int]): The Red, Green, Blue triplet.

    Returns:
        List[str]: The closest color names from the RGB value.
    """
    min_colors = {}

    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb[0])**2
        gd = (g_c - rgb[1])**2
        bd = (b_c - rgb[2])**2
        min_colors[(rd + gd + bd)] = name

    # Sort the keys based on the minimum values, indicating liklihood.
    min_colors = [
        min_colors[key] for key in sorted(min_colors.keys(), reverse=False)
    ]

    # Return the 3 most likely colors in order of likelihood.
    return min_colors[:3]
