import pygame
from help_functions import load_image


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
shadow_casters = pygame.sprite.Group()
decorations = pygame.sprite.Group()

tile_images = {
    'black': load_image('tile2.png'),
    'white': load_image('tile1.png'),
}
decoration_images = {
    'block': load_image('tile3.png'),
    'stone_wall': load_image('stone_wall.png'),
    'tree': load_image('tree.png')
}
player_image = load_image('MainCharacter.png')
