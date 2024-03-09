import pygame

from opengl_render_pipeline import Shader
from initialization import shadows_layer, size


class ShadowCaster:
    def __init__(self, image, angle):
        self.angle = angle
        self.shader = Shader('shaders/Shadow.vert', 'shaders/Shadow.frag',
                             size=(image.get_width() * 4, image.get_height() * 4), data={'in_angle': angle})
        self.shadow = self.make_shadow(image, self.angle)

    def setup_new_image(self, new_image):
        self.shadow = self.make_shadow(new_image, self.angle)

    def change_angle(self):
        pass

    def cast_shadow(self, pos_x, pos_y):
        shadows_layer.blit(self.shadow, (pos_x - self.shadow.get_width() // 2, pos_y - self.shadow.get_height()
                                         + 5 * self.shadow.get_height() // 4))

    def make_shadow(self, image, angle):
        upscale_image = pygame.Surface((image.get_width() * 4, image.get_height() * 4))
        upscale_image.blit(image, (image.get_width() * 2, image.get_height() * 3))

        img = self.shader.render(image=upscale_image, create_texture=True)
        img.set_colorkey((0, 0, 0))

        flipped = pygame.transform.flip(img, False, True)
        flipped.set_colorkey((0, 0, 0))

        return flipped


class GodRays:
    def __init__(self, angle, color, alpha):
        self.shaders = []
        self.obj = None
        self.god_rays = pygame.Surface((size[0], size[1]), pygame.SRCALPHA, 32)
        self.angle = angle
        self.alpha = alpha
        self.color = color

    def send_data_to_shader(self, data):
        for key, val in data.items():
            for i in self.shaders:
                i.shader_data[key] = val

    def create_god_rays(self, objects):
        self.obj = objects
        brightness = self.alpha / 255
        color = (self.color[0] / 255, self.color[1] / 255, self.color[2] / 255)
        image_width, image_height = size[0], size[1]
        for i in objects:
            img = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
            img.blit(i.image, (image_width // 2, image_height - i.image.get_height()))
            r, t, l, b = get_corners(img)
            right, top = r / image_width, t / image_height
            left, bottom = l / image_width, b / image_height
            depth_shader = Shader('shaders/DepthMap.vert', 'shaders/DepthMap.frag', img,
                                  data={'topRight': (right, top), 'bottomLeft': (left, bottom),
                                        'COLOR': color, 'brightness': brightness, 'dist': b / size[1], 'time': 0})
            self.shaders.append(depth_shader)

    def render(self):
        self.god_rays.fill((*self.color, 10))
        for n, i in enumerate(self.obj):
            img = self.shaders[n].render(create_texture=True)
            img.set_colorkey((0, 0, 0))
            self.god_rays.blit(img, (-size[0] // 2 + i.rect.x, -size[1] + i.image.get_height() + i.rect.y))


def get_corners(img):
    pixels = pygame.PixelArray(img)
    left = 1000
    right = -1
    top = 1000
    bottom = -1
    for i in range(img.get_height()):
        for j in range(img.get_width()):
            if pixels[j, i] != 0 and j > right:
                right = j
            elif pixels[j, i] != 0 and i < top:
                top = i
            elif pixels[j, i] != 0 and j < left:
                left = j
            elif pixels[j, i] != 0 and i > bottom:
                bottom = i
    return right, top, left, bottom
