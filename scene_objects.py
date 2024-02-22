import pygame
from sprites import tiles_group, all_sprites, tile_images, decoration_images, decorations, sort_by_y, shadow_casters
from constants import TILE_WIDTH, TILE_HEIGHT, GLOBAL_LIGHTNING_ANGLE
from global_lightning import ShadowCaster
from initialization import screen


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_id, pos_x, pos_y, x_offset=0, y_offset=0):
        super().__init__(tiles_group, all_sprites)
        self.image_id = image_id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.image = tile_images[image_id]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x + x_offset, TILE_HEIGHT * pos_y + y_offset)


class Decoration(pygame.sprite.Sprite):
    def __init__(self, image_id, pos_x, pos_y, casts_shadows=False):
        super().__init__(decorations, all_sprites, sort_by_y)
        self.image_id = image_id
        self.casts_shadows = casts_shadows
        self.image = decoration_images[image_id]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.sprite_y = self.image.get_rect().bottom
        self.mask = pygame.mask.from_surface(self.image)
        self.collider = self.create_collider()
        self.offset = (0, )
        if casts_shadows:
            self.shadow_caster = ShadowCaster(self.image, GLOBAL_LIGHTNING_ANGLE)
            shadow_casters.add(self)

    def create_collider(self):
        top, left, right, bottom = 1000, 1000, -1, -1
        pixels = pygame.PixelArray(self.image)
        for i in range(len(pixels)):
            for j in range(len(pixels[0])):
                if pixels[i, j] != 0:
                    left = j if j < left else left
                    right = j if j > right else right
                    top = i if i < top else top
                    bottom = i if i > bottom else bottom
        collider = pygame.Rect(self.rect.x + left, self.rect.y, right - left, self.rect.h)
        self.offset = (left, )
        return collider

    def update_collider(self):
        print(self.rect)
        print(self.collider)
        self.collider.x = self.rect.x + self.offset[0]
        self.collider.y = self.rect.y

    def update(self):
        self.update_collider()
        if self.casts_shadows:
            self.shadow_caster.cast_shadow(self.rect.x, self.rect.y)
