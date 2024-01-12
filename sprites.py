import pygame
from help_functions import load_image


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
shadow_casters = pygame.sprite.Group()
walls = pygame.sprite.Group()

tile_images = {
    'black': load_image('tile2.png'),
    'white': load_image('tile1.png'),
    'block': load_image('tile3.png')
}
player_image = load_image('MainCharacter.png')