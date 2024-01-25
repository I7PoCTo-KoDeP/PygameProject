import pygame

from opengl_render_pipeline import Shader
from initialization import shadows_layer, sunshafts_layer


class ShadowCaster:
    def __init__(self, image):
        self.shadow = self.make_shadow(image, 90)

    def make_shadow(self, image, angle):
        shader = Shader(image, 'shaders/vertex.glsl', 'shaders/fragment.glsl', {'in_angle': angle})

        image_res = pygame.Surface((image.get_height() * 2, image.get_width() * 2))
        image_res.blit(image, image.get_size())

        img = shader.render()
        img.set_colorkey((0, 0, 0))

        pattern = pygame.Surface(image_res.get_size())
        pattern.fill((1, 1, 1))

        img.blit(pattern, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        img.set_alpha(100)

        return img

    def setup_new_image(self, new_image):
        self.shadow = self.make_shadow(new_image, 90)

    def cast_shadow(self, pos_x, pos_y):
        shadows_layer.blit(self.shadow, (pos_x, pos_y))


class SunShafts:
    def __init__(self, angle, color, alpha):
        self.angle = angle
        self.alpha = alpha
        self.color = color

    def render(self):
        sunshafts_layer.fill((*self.color, self.alpha))
