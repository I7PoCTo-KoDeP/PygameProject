import pygame
from sprites import player_group, all_sprites, player_image, shadow_casters
from constants import SCALE, PLAYER_SPEED
from global_lightning import ShadowCaster


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, casts_shadows=True):
        super().__init__(player_group, all_sprites, shadow_casters)
        self.image = pygame.transform.scale(player_image, (SCALE * 80, SCALE * 80))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        if casts_shadows:
            self.shadow_caster = ShadowCaster(self.image)

    def move(self, direction_x, direction_y):
        self.rect.x += PLAYER_SPEED * direction_x
        self.rect.y += PLAYER_SPEED * direction_y

    def update(self):
        self.shadow_caster.cast_shadow(self.rect.x, self.rect.y)
