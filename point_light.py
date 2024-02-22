import pygame

from opengl_render_pipeline import Shader
from initialization import screen


class PointLight:
    # TODO: point light, spot light
    def __init__(self, position, radius, brightness):
        self.position = position
        self.radius = radius
        self.brightness = brightness
