import pygame

from opengl_render_pipeline import Shader
from initialization import screen
from sprites import all_sprites, light_sources, sort_by_y, shadow_casters
from pygame.math import Vector2


class PointLight(pygame.sprite.Sprite):
    # TODO: point light, spot light
    def __init__(self, position, radius, brightness, color):
        super().__init__(all_sprites, sort_by_y, light_sources)
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect().move(position)
        self.center = self.rect.center
        self.radius = radius
        self.brightness = brightness
        self.color = color
        self.shader = Shader('shaders/PointLight.vert', 'shaders/PointLight.frag',
                             size=(self.radius * 2, self.radius * 2))
        self.sprite_y = position[1]

    def render(self):
        light = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(light, self.color, (self.radius, self.radius), self.radius)
        light.set_alpha(self.brightness * 255)
        if pygame.sprite.spritecollideany(self, shadow_casters):
            for i in shadow_casters:
                if pygame.sprite.collide_mask(self, i):
                    left, right = i.collider.bottomleft, i.collider.bottomright
                    right_chord = 2 * (Vector2(right) - Vector2(self.center)) + Vector2(self.radius, -2.5 * self.radius)
                    left_chord = 2 * (Vector2(left) - Vector2(self.center)) + Vector2(self.radius, -2.5 * self.radius)
                    top_right = (right_chord[0], right_chord[1])
                    top_left = (left_chord[0], left_chord[1])
                    bottom_right = (right[0] - self.rect.topleft[0], right[1] - self.rect.topleft[1])
                    bottom_left = (left[0] - self.rect.topleft[0], left[1] - self.rect.topleft[1])
                    pygame.draw.polygon(light, (0, 0, 0, 255),
                                        [bottom_right, top_right, top_left, bottom_left])
        self.image.blit(light, (0, 0))
        img = self.shader.render(image=self.image, create_texture=True)
        img.set_colorkey((0, 0, 0))
        self.image = img
        '''light = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(light, self.color, (self.radius, self.radius), self.radius)
        light.set_alpha(255 * self.brightness)'''
