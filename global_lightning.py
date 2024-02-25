import pygame

from opengl_render_pipeline import Shader
from initialization import shadows_layer, sunshafts_layer, size


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
                                         + self.shadow.get_height() // 4))

    def make_shadow(self, image, angle):
        upscale_image = pygame.Surface((image.get_width() * 4, image.get_height() * 4))
        upscale_image.blit(image, (image.get_width() * 2, image.get_height() * 3))

        # shader = Shader('shaders/Shadow.vert', 'shaders/Shadow.frag', upscale_image, data={'in_angle': angle})

        img = self.shader.render(image=upscale_image, create_texture=True)
        img.set_colorkey((0, 0, 0))

        return img


class GodRays:
    # TODO: God Ray Renderer
    def __init__(self, angle, color, alpha):
        self.shaders = []
        self.rays_shaders = []
        self.rays = []
        self.obj = None
        self.depth_map = pygame.Surface((size[0], size[1]), pygame.SRCALPHA, 32)
        self.angle = angle
        self.alpha = alpha
        self.color = color

    def find_last_pixel(self, img):
        pixels = pygame.PixelArray(img)
        last = -1
        for i in range(img.get_height()):
            for j in range(img.get_width()):
                if pixels[j, i] != 0 and j > last:
                    last = j
        return last

    def create_god_rays(self, objects):
        self.create_depth_shader(objects)
        ray = pygame.Surface((size[0], size[1]), pygame.SRCALPHA, 32)
        pygame.draw.rect(ray, (255, 128, 0, 0), (0, 0, 20, size[1]))
        shader = Shader('shaders/GodRays.vert', 'shaders/GodRays.frag', sprite=self.depth_map,
                        data={'TIME': 0})
        self.rays = shader.render()
        self.rays_shaders = shader
        self.obj = objects

    def send_data_to_shader(self, data):
        for key, val in data.items():
            self.rays_shaders.shader_data[key] = val

    def create_depth_shader(self, objects):
        for i in objects:
            image_height, image_width = i.image.get_height(), i.image.get_width()
            img = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
            img.blit(i.image, (0, 0))
            offset = self.find_last_pixel(i.image) / image_width
            depth_shader = Shader('shaders/DepthMap.vert', 'shaders/DepthMap.frag', img, data={'offset': offset})
            self.shaders.append(depth_shader)

    def render_depth_map(self, objects):
        self.depth_map.fill((0, 0, 0, 0))
        for n, i in enumerate(objects):
            img = self.shaders[n].render(create_texture=True)
            img.set_colorkey((0, 0, 0))
            self.depth_map.blit(img, (i.rect.x, i.rect.y))

    def render(self):
        self.depth_map.fill((0, 0, 0, 0))
        sunshafts_layer.fill((0, 0, 0, 0))

        self.render_depth_map(self.obj)
        sunshafts_layer.blit(self.rays_shaders.render(create_texture=True), (0, 0))
