from google.cloud import vision
from google.cloud.vision import types

import webcolors


class Analyzer:

    # def __init__(self):
    # self.client = vision.ImageAnnotatorClient()
    # self.image = types.Image()
    # self.image.source.image_uri = "gs://object-is.appspot.com/" + image_path
    # self.image.source.image_uri = "gs://object-is.appspot.com/"

    def analyze(self):
        self.detect_labels()
        self.detect_logos()
        self.detect_crop_hints()
        return self.detect_properties()

    def detect_labels(self):
        response = self.client.label_detection(image=self.image)
        labels = response.label_annotations
        print(labels)

    def detect_logos(self):
        response = self.client.logo_detection(image=self.image)
        logos = response.logo_annotations
        print(logos)

    def detect_properties(self):

        def get_rgb(color):
            return (int(color.color.red), int(color.color.green),
                    int(color.color.blue))

        def get_product(color):
            if color == "red":
                return "heima"
            elif color == "green":
                return "vor"
            else:
                return "haust"

        response = self.client.image_properties(image=self.image)
        properties = response.image_properties_annotation

        primary_color = self.get_color(
            get_rgb(properties.dominant_colors.colors[0]))
        secondary_color = self.get_color(
            get_rgb(properties.dominant_colors.colors[1]))
        print(primary_color, secondary_color)
        return get_product(primary_color)

    def get_color(rgb):
        print(rgb)

        def closest_color(requested_color):
            min_colors = {}
            for key, name in webcolors.css3_hex_to_names.items():
                r_c, g_c, b_c = webcolors.hex_to_rgb(key)
                rd = (r_c - requested_color[0])**2
                gd = (g_c - requested_color[1])**2
                bd = (b_c - requested_color[2])**2
                min_colors[(rd + gd + bd)] = name
            return min_colors[min(min_colors.keys())]

        def get_color_name(requested_color):
            try:
                closest_name = actual_name = webcolors.rgb_to_name(
                    requested_color)
            except ValueError:
                closest_name = closest_color(requested_color)
                actual_name = None
            return actual_name, closest_name

        actual, closest = get_color_name(rgb)

        return actual or closest

    def detect_crop_hints(self):
        crop_hints_params = types.CropHintsParams(aspect_ratios=[1.77])
        image_context = types.ImageContext(crop_hints_params=crop_hints_params)

        response = self.client.crop_hints(
            image=self.image, image_context=image_context)
        hints = response.crop_hints_annotation.crop_hints

        for n, hint in enumerate(hints):
            print('\nCrop Hint: {}'.format(n))

            vertices = ([
                '({},{})'.format(vertex.x, vertex.y)
                for vertex in hint.bounding_poly.vertices
            ])

            print('bounds: {}'.format(','.join(vertices)))
