import pygame

from opengl_render_pipeline import PostProcessing, Shader
from initialization import screen, size, ground_layer, shadows_layer, sunshafts_layer
from sprites import all_sprites, player_group, tiles_group, decorations
from constants import X_OFFSET, FPS
from player import Player
from global_lightning import SunShafts
from scene_objects import Decoration, Tile


sc_shader = PostProcessing(size, screen, 'shaders/vertex_screen_shader.glsl', 'shaders/fragment_screen_shader.glsl')
sunshafts = SunShafts(100)


def load_field(rows, columns):
    tiles = []
    for i in range(-1, rows):
        for j in range(-1, columns):
            if j % 2 == 0:
                color = 'white'
                offset = X_OFFSET
            else:
                color = 'black'
                offset = 0
            tile = Tile(color, i, j, offset)
            tiles.append(tile)


if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()

    load_field(20, 20)
    wall = Decoration('stone_wall', 459, 59, True)
    tree = Decoration('tree', 180, 170, True)
    player = Player(100, 100)

    while running:
        sunshafts.render()
        screen.fill(pygame.Color('white'))

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            player.move(-1, 0)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            player.move(1, 0)
        if pygame.key.get_pressed()[pygame.K_UP]:
            player.move(0, -1)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            player.move(0, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pass

        all_sprites.update()

        tiles_group.draw(ground_layer)
        screen.blit(ground_layer, (0, 0))
        screen.blit(sunshafts_layer, (0, 0))
        screen.blit(shadows_layer, (0, 0))
        shadows_layer.fill((1, 1, 1, 0))

        #test = pygame.Surface(size)
        #shader = Shader(screen, 'shaders/vertex_screen_shader.glsl', 'shaders/shadow_shader.glsl')

        player_group.draw(screen)
        decorations.draw(screen)

        sc_shader.render()

        pygame.display.flip()

        clock.tick(FPS)
