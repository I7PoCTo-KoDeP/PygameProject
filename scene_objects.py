import pygame
from sprites import tiles_group, all_sprites, tile_images
from constants import TILE_WIDTH, TILE_HEIGHT, SCALE


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, x_offset=0, y_offset=0):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (SCALE * 80, SCALE * 80))
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x + x_offset, TILE_HEIGHT * pos_y + y_offset)


class Decoration(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (SCALE * 80, SCALE * 80))
        self.rect = self.image.get_rect().move(pos_x, pos_y)
