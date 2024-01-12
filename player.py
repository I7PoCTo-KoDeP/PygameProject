import pygame
from sprites import player_group, all_sprites, player_image, shadow_casters
from constants import SCALE
from global_lightning_script import ShadowCaster


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, casts_shadows=True):
        super().__init__(player_group, all_sprites, shadow_casters)
        self.image = pygame.transform.scale(player_image, (SCALE * 80, SCALE * 80))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        if casts_shadows:
            self.shadow_caster = ShadowCaster(self.image)

    def move(self, direction_x, direction_y):
        self.rect.x += 1 * direction_x
        self.rect.y += 1 * direction_y

    def cast_shadow(self):
        self.shadow_caster.cast_shadow(self.rect.x, self.rect.y)

    def update(self):
        self.shadow_caster.cast_shadow(self.rect.x - 160, self.rect.y + 160)
