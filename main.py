import pygame

from opengl_render_pipeline import PostProcessing, Shader
from initialization import screen, size, ground_layer, shadows_layer, sunshafts_layer
from sprites import all_sprites, tiles_group, sort_by_y
from constants import X_OFFSET, FPS, PLAYER_START_SPEED, PLAYER_MAX_SPEED
from player import Player
from camera import Camera
from global_lightning import SunShafts
from scene_objects import Decoration, Tile


sc_shader = PostProcessing(size, screen, 'shaders/vertex_screen_shader.glsl', 'shaders/fragment_screen_shader.glsl')
sunshafts = SunShafts(100, (120, 120, 100), 100)
camera = Camera(size, (0, 40))


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


def clear_layer(layer):
    layer.fill((255, 255, 255, 255))


if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()

    direction = [0, 0]

    load_field(20, 20)
    wall = Decoration('stone_wall', 180, 59, True)
    tree = Decoration('tree', 10, 10, True)
    player = Player(100, 100)

    while running:
        sunshafts.render()
        clear_layer(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pass

        player.move(PLAYER_MAX_SPEED, PLAYER_START_SPEED)

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        all_sprites.update()

        tiles_group.draw(ground_layer)
        screen.blit(ground_layer, (0, 0))
        #screen.blit(sunshafts_layer, (0, 0))
        screen.blit(shadows_layer, (0, 0))
        shadows_layer.fill((1, 1, 1, 0))

        clear_layer(ground_layer)

        # test = pygame.Surface(size)
        # shader = Shader(screen, 'shaders/vertex_screen_shader.glsl', 'shaders/shadow_shader.glsl')

        sort_by_y.draw(screen)

        sc_shader.render()

        pygame.display.flip()

        clock.tick(FPS)
