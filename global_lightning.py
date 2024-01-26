import pygame

from opengl_render_pipeline import Shader
from initialization import shadows_layer, sunshafts_layer


class ShadowCaster:
    def __init__(self, image):
        self.angle = 30
        self.shadow = self.make_shadow(image, self.angle)

    def setup_new_image(self, new_image):
        self.shadow = self.make_shadow(new_image, self.angle)

    def change_angle(self):
        pass

    def cast_shadow(self, pos_x, pos_y):
        shadows_layer.blit(self.shadow, (pos_x - self.shadow.get_width() // 2, pos_y - self.shadow.get_height()
                                         + self.shadow.get_height() // 4))

    def make_shadow(self, image, angle):
        upscale_image = pygame.Surface((image.get_width() * 4, image.get_height() * 4))
        upscale_image.blit(image, (image.get_width() * 2, image.get_height() * 3))

        shader = Shader(upscale_image, 'shaders/vertex.glsl', 'shaders/fragment.glsl', {'in_angle': angle})
        shader.send_data()

        img = shader.render()
        img.set_colorkey((0, 0, 0))

        pattern = pygame.Surface(upscale_image.get_size())
        pattern.fill((1, 1, 1))

        img.blit(pattern, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        img.set_alpha(100)

        return img


class SunShafts:
    def __init__(self, angle, color, alpha):
        self.shader = Shader(shadows_layer, '', '')
        self.angle = angle
        self.alpha = alpha
        self.color = color

    def render(self):
        sunshafts_layer.fill((*self.color, self.alpha))
