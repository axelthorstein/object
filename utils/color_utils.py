#pylint: disable=too-many-return-statements,too-many-branches
import colorsys
import webcolors


class ColorException(Exception):
    pass


COLOR_MAP = {
    'red': '00',
    'orange': '01',
    'yellow': '02',
    'lime': '03',
    'green': '04',
    'turquoise': '05',
    'cyan': '06',
    'lightblue': '07',
    'blue': '08',
    'purple': '09',
    'magenta': '10',
    'pink': '11'
}


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
            code += COLOR_MAP[color]
    except ValueError:
        raise ColorException(f"Color {color} not found.")

    return code


def get_hue_name(hue):
    """Get the name of a hue.

    Args:
        hue (int): The value of a hue from a HSV tuple.

    Returns:
        str: The color name from the hue value.
    """
    if 0 <= hue <= 15:
        return 'red'
    elif 15 < hue <= 45:
        return 'orange'
    elif 45 < hue <= 70:
        return 'yellow'
    elif 70 < hue <= 90:
        return 'lime'
    elif 90 < hue <= 145:
        return 'green'
    elif 145 < hue <= 160:
        return 'turquoise'
    elif 160 < hue <= 185:
        return 'cyan'
    elif 185 < hue <= 210:
        return 'lightblue'
    elif 210 < hue <= 260:
        return 'blue'
    elif 260 < hue <= 275:
        return 'purple'
    elif 275 < hue <= 300:
        return 'magenta'
    elif 300 < hue <= 330:
        return 'pink'
    elif 330 < hue <= 360:
        return 'red'


def get_color(rgb):
    """Get the name of a color for a RGB value.

    Resolve the human readable names for a RBG value. This method is a great
    speed increase over the `get_most_likely_colors` method, however it assumes
    that the hue is the exact color name and is limited to 16 colors (for now).

    TODO: Add back grey checking.

    Args:
        rgb (List[int]): The Red, Green, Blue triplet.

    Returns:
        List[str]: The color name from the RGB value.
    """
    hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    hue = int(hsv[0] * 360)
    saturation = hsv[1]
    brightness = hsv[2] / 255
    color_name = get_hue_name(hue)

    if brightness < 0.3:
        color = 'black'
    elif saturation < 0.05 and brightness > 0.95:
        color = 'white'
    # elif (saturation < 0.05 and brightness > 0.30) or (saturation < 0.1 and brightness < 0.50):
    #     color = 'grey'
    # elif brightness < 0.75:
    #     color = 'dark-' + color_name
    # elif saturation < 0.75 and brightness > 0.95:
    #     color = 'light-' + color_name
    else:
        color = color_name

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
