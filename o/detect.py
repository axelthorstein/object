import os
import cv2
import matplotlib.image
from PIL import Image
import numpy as np

from o.analyzer import Analyzer
# from analyzer import Analyzer
import webcolors



class Ring:
    """
    A ring object with a center point, and a distance radius to it's inner
    and outer rings.
    """

    def __init__(self, image, image_path, inner_circle, outer_circle):
        self.image = image
        self.image_path = image_path
        self.center_coords = (inner_circle[0], inner_circle[1])
        self.inner_radius = inner_circle[2]
        self.outer_radius = outer_circle[2]
        self.is_ring = (outer_circle[2] - inner_circle[2]) > 2
        self.colors = self.get_colors()

    def get_rgb(self, rgb):
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def get_secondary_color(self, image, primary_color):
        """
        The while will go out of bounds if the ring is too close to the top.
        """
        if self.is_ring:
            secondary_color = Analyzer.get_color(self.get_rgb(image[self.center_coords[0]][self.center_coords[1]]))
        else:
            offset = self.outer_radius + 1
            secondary_color = Analyzer.get_color(self.get_rgb(image[self.center_coords[0]][self.center_coords[1] + offset]))

            while secondary_color == primary_color:
                offset += 10
                secondary_color = Analyzer.get_color(self.get_rgb(image[self.center_coords[0]][self.center_coords[1] + offset]))

        return secondary_color

    def get_rgb_coords(self):
        if self.is_ring:
            return (self.center_coords[0], ((self.outer_radius - self.inner_radius) // 2)
                    + self.inner_radius + self.center_coords[1])
        else:
            return (self.center_coords[0], self.inner_radius // 2 + self.center_coords[1])

    def get_colors(self):
        image = matplotlib.image.imread(self.image_path)

        rgb_coords = self.get_rgb_coords()

        primary_color = Analyzer.get_color(self.get_rgb(image[rgb_coords[0]][rgb_coords[1]]))
        secondary_color = self.get_secondary_color(image, primary_color)
        
        return (primary_color, secondary_color)

    def to_string(self):
        return "Detected a ring at the coordinates {} with a inner and \
outer radius of {} from {}.".format(
               self.center_coords, (self.inner_radius, self.outer_radius),
               os.path.basename(self.image_path).replace("_thumbnail.png", ""))

class Detect:
    """
    Detect a circle from a given image.
    """

    def __init__(self, image_path):
        self.image_path = self.crop(image_path)

    def crop(self, image_path):
        cropped_path = image_path[:-4] + "_thumbnail.png"
        image = Image.open(image_path)
        half_the_width = image.size[0] / 2
        half_the_height = image.size[1] / 2

        # TODO: Will need to adjust these values to match the actual overlay.
        # cropped_image = image.crop(
        #     (
        #         half_the_width - (half_the_width * 0.35),
        #         half_the_height - (half_the_height * 0.15),
        #         half_the_width + (half_the_width * 0.3),
        #         half_the_height + (half_the_height * 0.7)
        #     )
        # )
        cropped_image = image
        cropped_image.save(cropped_path)
        self.image_width = cropped_image.size[0]
        self.center_pixel = int(self.image_width / 2)

        return self.compress(cropped_path)

    def compress(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((self.image_width, self.image_width), Image.ANTIALIAS)
        image.save(image_path)
        
        return image_path

    def get_ring(self, img):
        x = 0
        y = 1

        def get_colour_name(rgb_triplet):
            min_colours = {}
            for key, name in webcolors.css21_hex_to_names.items():
                r_c, g_c, b_c = webcolors.hex_to_rgb(key)
                rd = (r_c - rgb_triplet[0]) ** 2
                gd = (g_c - rgb_triplet[1]) ** 2
                bd = (b_c - rgb_triplet[2]) ** 2
                min_colours[(rd + gd + bd)] = name
            return min_colours[min(min_colours.keys())]

        def rgb(coords):
            return tuple(img[coords[x], coords[y]])

        def color(coords):
            return get_colour_name(rgb(coords))

        def walk(starting_coords, direction):
            starting_color = color(starting_coords)
            next_coords = starting_coords
            next_color = color(direction(next_coords))

            while next_color == starting_color:
                next_coords = direction(next_coords)
                next_color = color(direction(next_coords))

            print("Walked {}, starting color: {} at {}, next color: {} at {}".format(direction.__name__, starting_color, starting_coords, next_color, next_coords))

            return next_coords

        def up(coords):
            return (coords[x], coords[y] + 1)

        def down(coords):
            return (coords[x], coords[y] - 1)

        def left(coords):
            return (coords[x] - 1, coords[y])

        def right(coords):
            return (coords[x] + 1, coords[y])

        starting_center_coords = [self.center_pixel, self.center_pixel]

        left_coords = walk(starting_center_coords, left)
        right_coords = walk(starting_center_coords, right)
        up_coords = walk(starting_center_coords, up)
        down_coords = walk(starting_center_coords, down)

        center_x = left_coords[x] + (int(right_coords[x] - left_coords[x]) / 2)
        center_y = down_coords[y] + (int(up_coords[y] - down_coords[y]) / 2)
        center_coords = (int(center_x), int(center_y))

        inner_radius = right_coords[x] - center_coords[x]
        outer_radius = walk(right(right_coords), right)[x] - center_coords[x]

        print("Center point {}, inner radius: {}, outer radius: {}".format(center_coords, inner_radius, outer_radius))

        self.draw_ring(img, center_coords, inner_radius, outer_radius)

        center_color = color(center_coords)
        ring_color = color((center_coords[x] + inner_radius + int((outer_radius - inner_radius) / 2), center_coords[y]))

        return (center_color, ring_color)

    def draw_ring(self, img, center_coords, inner_radius, outer_radius):
        cv2.circle(img, center_coords, inner_radius, (0, 255, 0), 1)
        cv2.circle(img, center_coords, outer_radius, (0, 255, 0), 1)
        cv2.circle(img, center_coords, 2, (255, 0, 0), 1)
        cv2.imwrite("/Users/axelthor/Projects/object/images/test_draw.png", img)
        
    def detect_circle(self):
        img = cv2.imread(self.image_path)
        img = cv2.bilateralFilter(img,9,75,75)

        ring = self.get_ring(img)

        exit()


class Detect_hard:
    """
    Detect a circle from a given image.
    """

    def __init__(self, image_path):
        self.image_path = self.compress(image_path)

    def compress(self, image_path):
        thumbnail_path = image_path[:-4] + "_thumbnail.png"
        image = Image.open(image_path)
        image.thumbnail((256, 256), Image.ANTIALIAS)
        image.save(thumbnail_path)
        
        return thumbnail_path

    def get_ring(self, img):

        def round(nums, precision=0):
            return np.uint16(np.around(nums, precision))

        # print(cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, .5, 20, 30, 30, 10, 10))

        c1 = round(cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, .5, 10, 10, 10, 10, 10)[0][0])
        c2 = round(cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.5, 10, 10, 10, 10, 10)[0][0])

        if c1[2] > c2[2]:
            outer_circle = c1
            inner_circle = c2
        else:
            outer_circle = c2
            inner_circle = c1

        if round(inner_circle[0:1], -1) == round(outer_circle[0:1], -1):
            return Ring(img, self.image_path, inner_circle, outer_circle)

    def draw_ring(self, ring, img): 
        gray_scale = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        if ring.outer_radius != ring.inner_radius:
            # Draw the outer circle
            cv2.circle(gray_scale, ring.center_coords, ring.outer_radius, (0, 255, 0), 2)
            # Draw the inner circle
            cv2.circle(gray_scale, ring.center_coords, ring.inner_radius, (255, 0, 0), 2)
        else:
            cv2.circle(gray_scale, ring.center_coords, ring.inner_radius, (255, 255, 0), 2)

        # Draw the center of the circle
        cv2.circle(gray_scale, ring.center_coords, 2, (0 , 0, 255), 3)

        cv2.imwrite(self.image_path, gray_scale)
        
    def detect_circle(self):
        img = cv2.imread(self.image_path, 0)
        img = cv2.medianBlur(img, 5)
        ring = self.get_ring(img)

        if ring:
            print(ring.to_string())
            self.draw_ring(ring, img)
            return ring.get_colors()
        else:
            print("No circles detected.")
        
        # os.remove(self.image_path)


if __name__=="__main__":
    Detect("/Users/axelthor/Projects/object/images/test.png").detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/ring.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/thick_ring.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/two_rings.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/moon_ring.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/circle.png').detect_circle()
    # Detect('/Users/axelthor/Projects/object/images/moon.png').detect_circle()
