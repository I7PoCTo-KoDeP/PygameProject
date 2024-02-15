import pygame

from opengl_render_pipeline import Shader
from initialization import shadows_layer, sunshafts_layer, size


class ShadowCaster:
    def __init__(self, image, angle):
        self.angle = angle
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

        shader = Shader('shaders/Shadow.vert', 'shaders/Shadow.frag', upscale_image, data={'in_angle': angle})

        img = shader.render()
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
        '''for _ in objects:
            img = pygame.Surface((size[0], size[1]))
            #shader = Shader('shaders/GodRays.vert', 'shaders/GodRays.frag', sprite=img, data={'TIME': 0})
            shader = Shader('shaders/Default.vert', 'shaders/Default.frag', sprite=img)
            self.shaders.append(shader)'''
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
            #print(offset)
            depth_shader = Shader('shaders/DepthMap.vert', 'shaders/DepthMap.frag', img, data={'offset': offset})
            self.shaders.append(depth_shader)

    def render_depth_map(self, objects):
        self.depth_map.fill((0, 0, 0, 0))
        for n, i in enumerate(objects):
            img = self.shaders[n].render(create_texture=True)
            img.set_colorkey((0, 0, 0))
            self.depth_map.blit(img, (i.rect.x, i.rect.y))
            #self.depth_map.blit(shadows, (0, 0))
            #color = pygame.Surface(size, pygame.SRCALPHA)
            #color.fill((0, 0, 0))
            #self.depth_map.blit(color, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def render(self):
        self.depth_map.fill((0, 0, 0, 0))
        sunshafts_layer.fill((0, 0, 0, 0))

        self.render_depth_map(self.obj)
        '''for i in self.obj:
            self.depth_map.blit(i.image, (i.rect.x, i.rect.y))
        rays = [shader.render() for shader in self.rays_shaders]
        coords = [i.rect for i in self.obj]
        for obj, shader in zip(self.obj, self.shaders):
            shader.blit_image(obj.image, obj.rect)
        images = [shader.render() for shader in self.shaders]
        for image, coord in zip(images, coords):
            for i in rays:
                image.blit(i, (coord[0], 0))
            image.set_colorkey((0, 0, 0))
            sunshafts_layer.blit(image, (0, 0))
        for img, coord in zip(rays, coords):'''
        sunshafts_layer.blit(self.rays_shaders.render(create_texture=True), (0, 0))
