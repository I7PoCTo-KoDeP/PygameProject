import pygame
from sprites import tiles_group, all_sprites, tile_images, decoration_images, decorations
from constants import TILE_WIDTH, TILE_HEIGHT, SCALE
from global_lightning import ShadowCaster


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, x_offset=0, y_offset=0, casts_shadows=False):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (SCALE * 80, SCALE * 80))
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x + x_offset, TILE_HEIGHT * pos_y + y_offset)


class Decoration(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, casts_shadows=False):
        super().__init__(decorations, all_sprites)
        self.image = pygame.transform.scale(decoration_images[tile_type], (SCALE * 128, SCALE * 128))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.casts_shadows = casts_shadows
        if casts_shadows:
            self.shadow_caster = ShadowCaster(self.image)

    def update(self):
        if self.casts_shadows:
            self.shadow_caster.cast_shadow(self.rect.x, self.rect.y)
