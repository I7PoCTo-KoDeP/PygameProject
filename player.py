import pygame
from math import exp
from sprites import player_group, all_sprites, player_image, shadow_casters, sort_by_y
from global_lightning import ShadowCaster
from help_functions import clamp
from constants import GLOBAL_LIGHTNING_ANGLE


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, casts_shadows=True):
        super().__init__(player_group, all_sprites, shadow_casters, sort_by_y)
        self.image = player_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.current_speed = 0
        self.sprite_y = self.image.get_rect().bottom
        self.flipped = False
        if casts_shadows:
            self.shadow_caster = ShadowCaster(self.image, GLOBAL_LIGHTNING_ANGLE)

    def flip(self, x_direction):
        if x_direction < 0 and not self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = True
        if x_direction > 0 and self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = False
        self.shadow_caster.setup_new_image(self.image)

    def move(self, max_speed, acceleration):
        direction_x, direction_y = self.get_direction()
        if direction_x == 0 and direction_y == 0:
            self.stop(acceleration)
        self.current_speed = self.calculate_speed(max_speed, 0.2, 2)
        self.rect.x += self.current_speed * direction_x
        self.rect.y += self.current_speed * direction_y

    def calculate_speed(self, max_speed, smoothness, exp_pow=1):
        speed = clamp(0, max_speed, self.current_speed * exp(exp_pow) * smoothness)
        return speed

    def stop(self, acceleration):
        self.current_speed = acceleration

    def get_direction(self):
        direction = [0, 0]
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            direction[0] = -1
            self.flip(-1)
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            direction[0] = 1
            self.flip(1)
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            direction[1] = -1
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            direction[1] = 1
        return direction

    def update(self):
        self.shadow_caster.cast_shadow(self.rect.x, self.rect.y)
