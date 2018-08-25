import numpy
import colorsys
from profilehooks import timecall
# from PIL import Image

# def median_filter(data, filter_size):
#     temp = []
#     indexer = filter_size // 2
#     data_final = []
#     data_final = numpy.zeros((len(data),len(data[0])))
#     for i in range(len(data)):

#         for j in range(len(data[0])):

#             for z in range(filter_size):
#                 if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
#                     for c in range(filter_size):
#                         temp.append(0)
#                 else:
#                     if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
#                         temp.append(0)
#                     else:
#                         for k in range(filter_size):
#                             temp.append(data[i + z - indexer][j + k - indexer])

#             temp.sort()
#             data_final[i][j] = temp[len(temp) // 2]
#             temp = []
#     return data_final

# def main():
#     img = Image.open("tests/test_images/real_test_circle.png").convert(
#         "L")
#     arr = numpy.array(img)
#     removed_noise = median_filter(arr, 3)
#     img = Image.fromarray(removed_noise)
#     img.show()

# main()

from PIL import Image

# from utils.color_utils import get_color

# def median_filter(image, filter_size):
#     temp = []
#     width, height = image.size
#     pixel_matrix = image.load()
#     indexer = filter_size // 2
#     data_final = []

#     for j in range(width):
#         column = []
#         for i in range(height):
#                 column.append(0)
#         data_final.append(column)

#     for i in range(width):

#         for j in range(height):

#             for z in range(filter_size):
#                 if i + z - indexer < 0 or i + z - indexer > width - 1:
#                     for c in range(filter_size):
#                         temp.append('0')
#                 else:
#                     if j + z - indexer < 0 or j + indexer > height - 1:
#                         temp.append('0')
#                     else:
#                         for k in range(filter_size):
#                             x_index = i + k - indexer
#                             y_index = j + z - indexer
#                             if x_index < 0:
#                                 x_index = width - 1
#                             if y_index < 0:
#                                 y_index = height - 1
#                             print(x_index, y_index)
#                             temp.append(get_color(pixel_matrix[x_index, y_index])[0])
#             # import ipdb;ipdb.set_trace()

#             temp.sort()

#             data_final[i][j] = temp[len(temp) // 2]
#             temp = []

#     return data_final

# def main():
#     image = Image.open("tests/test_images/real_test_circle.png")
#     list_of_pixels = median_filter(image, 3)
#     im2 = Image.new(im.mode, im.size)
#     im2.putdata(list_of_pixels)
#     im2.show()

# main()


def name_to_rgb(name):
    color_ranges_map = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'blue': (0, 0, 255),
        'green': (0, 255, 0),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'orange': (255, 165, 0)
    }
    return color_ranges_map[name]


def generate_color_range_map():
    color_range_map = {}
    color_ranges_map = {
        range(0, 45): 'orange',
        range(45, 80): 'yellow',
        range(80, 150): 'green',
        range(150, 195): 'cyan',
        range(195, 255): 'blue',
        range(255, 315): 'magenta',
        range(315, 360): 'red'
    }

    for color_range in color_ranges_map:
        for value in color_range:
            color_range_map[value] = color_ranges_map[color_range]

    return color_range_map


COLOR_RANGES_MAP = generate_color_range_map()


def get_hue_name(hue):
    """Get the name of a hue.

    Args:
        hue (int): The value of a hue from a HSV tuple.

    Returns:
        str: The color name from the hue value.

    Raises:
        ColorException: If the hue isn't in any color range.
    """

    return COLOR_RANGES_MAP[hue]


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
    elif saturation < 0.2 and brightness > 0.75:
        color = 'white'
    # elif ((saturation < 0.25 and brightness < 0.40) or
    #       (saturation < 0.15 and brightness < 0.80)):
    #     color = 'grey'
    else:
        color = get_hue_name(hue)

    return [color]


# Create a Primary Colors version of the image
@timecall
def convert_primary(image):
    # Get size
    width, height = image.size

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()

    # Transform to primary
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixel = get_pixel(image, i, j)
            pixels[i, j] = name_to_rgb(get_color(pixel)[0])

            # # Get R, G, B values (This are int from 0 to 255)
            # red = pixel[0]
            # green = pixel[1]
            # blue = pixel[2]

            # # Transform to primary
            # if red > 127:
            #     red = 255
            # else:
            #     red = 0
            # if green > 127:
            #     green = 255
            # else:
            #     green = 0
            # if blue > 127:
            #     blue = 255
            # else:
            #     blue = 0

            # # Set Pixel in new image
            # pixels[i, j] = (int(red), int(green), int(blue))

    # Return new image
    return new


def open_image(path):
    newImage = Image.open(path)
    return newImage


# Save Image
def save_image(image, path):
    image.save(path, 'png')


# Create a new image with the given size
def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image


# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel


original = open_image('tests/test_images/real_test_circle.png')
# Convert to Primary and save
new = convert_primary(original)
save_image(new, 'images/debug.png')
