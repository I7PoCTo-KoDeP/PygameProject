import pygame

from opengl_render_pipeline import PostProcessing
from initialization import screen, size, ground_layer, shadows_layer, sunshafts_layer, objects_layer
from sprites import all_sprites, tiles_group, sort_by_y, shadow_casters
from constants import X_OFFSET, FPS, PLAYER_START_SPEED, PLAYER_MAX_SPEED, GLOBAL_LIGHTNING_ANGLE
from player import Player
from camera import Camera
from global_lightning import GodRays
from scene_objects import Decoration, Tile


sc_shader = PostProcessing(size, screen, 'shaders/Screen.vert', 'shaders/Screen.frag')
god_rays = GodRays(GLOBAL_LIGHTNING_ANGLE, (120, 120, 100), 100)
camera = Camera(size, (0, 40))
time = 0


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
    layer.fill((255, 255, 255, 0))


if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()

    direction = [0, 0]

    load_field(20, 20)
    wall = Decoration('stone_wall', 180, 59, True)
    tree = Decoration('tree', 10, 10, True)
    player = Player(100, 100)

    god_rays.create_god_rays(shadow_casters)

    while running:
        time += 0.05
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

        # Frame formation
        sort_by_y.draw(objects_layer)
        tiles_group.draw(ground_layer)
        screen.blit(ground_layer, (0, 0))
        screen.blit(shadows_layer, (0, 0))
        screen.blit(objects_layer, (0, 0))
        #god_rays.render_depth_map(shadow_casters)
        #screen.blit(god_rays.depth_map, (0, 0))

        # Post-processing
        #shader_data = {'TIME': time}
        #god_rays.send_data_to_shader(shader_data)
        #god_rays.render()
        #screen.blit(sunshafts_layer, (0, 0))

        # Clearing
        clear_layer(ground_layer)
        clear_layer(objects_layer)
        shadows_layer.fill((1, 1, 1, 0))

        sc_shader.render()

        pygame.display.flip()

        clock.tick(FPS)
