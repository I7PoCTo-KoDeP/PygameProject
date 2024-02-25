import pygame

from opengl_render_pipeline import Shader
from initialization import screen
from sprites import all_sprites, light_sources


class PointLight(pygame.sprite.Sprite):
    # TODO: point light, spot light
    def __init__(self, position, radius, brightness, color):
        super().__init__(all_sprites, light_sources)
        light = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(light, color, (radius, radius), radius)
        light.set_alpha(brightness * 255)
        self.center = position[0] + radius, position[1] + radius
        self.image = light
        self.rect = self.image.get_rect().move(position)
        self.radius = radius
        self.brightness = brightness
        self.color = color
        self.shader = Shader('shaders/PointLight.vert', 'shaders/PointLight.frag',
                             size=(self.radius * 2, self.radius * 2))

    def render(self):
        light = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(light, self.color, (self.radius, self.radius), self.radius)
        light.set_alpha(255 * self.brightness)
