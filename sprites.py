import pygame
from help_functions import load_image


class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, position):
        super().__init__(*groups)


class SortingByY(pygame.sprite.Group):
    def by_y(self, sprite):
        return sprite.rect.y + sprite.sprite_y

    def draw(self, surface, **kwargs):
        sprites = self.sprites()
        surface_blit = surface.blit
        for sprite in sorted(sprites, key=self.by_y):
            self.spritedict[sprite] = surface_blit(sprite.image, sprite.rect)
        self.lostsprites = []


sort_by_y = SortingByY()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
shadow_casters = pygame.sprite.Group()
decorations = pygame.sprite.Group()
save_group = pygame.sprite.Group()

tile_images = {
    0: load_image('Tile2.png'),
    1: load_image('Tile1.png'),
}
decoration_images = {
    0: load_image('Tile3.png'),
    1: load_image('Stone_wall.png'),
    2: load_image('Tree.png')
}
player_image = load_image('MainCharacter.png')
player_run = load_image('MainCharacter_run.png')
