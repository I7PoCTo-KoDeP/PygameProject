import pygame
from help_functions import load_image


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
    0: load_image('tile2.png'),
    1: load_image('tile1.png'),
}
decoration_images = {
    0: load_image('tile3.png'),
    1: load_image('stone_wall.png'),
    2: load_image('tree.png')
}
player_image = load_image('MainCharacter.png')
player_run = load_image('MainCharacter_run.png')
