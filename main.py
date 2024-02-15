import pygame

from opengl_render_pipeline import PostProcessing
from initialization import screen, size, ground_layer, shadows_layer, sunshafts_layer, objects_layer
from sprites import all_sprites, tiles_group, sort_by_y, shadow_casters, save_group
from constants import *
from player import Player
from camera import Camera
from global_lightning import GodRays
from save_module import save, load_save
from help_functions import clear_layer, load_map
from scene_objects import Tile, Decoration


sc_shader = PostProcessing(size, screen, 'shaders/Screen.vert', 'shaders/Screen.frag')
god_rays = GodRays(GLOBAL_LIGHTNING_ANGLE, (120, 120, 100), 100)
camera = Camera(size, (0, 40))
time = 0


if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()

    objects = load_map('maps/game_map.json')
    for i in objects:
        eval(i)

    save_data = load_save()
    if save_data is not None:
        player = eval(save_data[0])
    else:
        player = Player(0, 0)

    god_rays.create_god_rays(shadow_casters)

    direction = [0, 0]

    while running:
        time += 0.05
        clear_layer(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    save(save_group)

        player.move(PLAYER_MAX_SPEED, PLAYER_START_SPEED)

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        all_sprites.update()

        # Frame Formation
        sort_by_y.draw(objects_layer)
        tiles_group.draw(ground_layer)
        screen.blit(ground_layer, (0, 0))
        screen.blit(shadows_layer, (0, 0))
        screen.blit(objects_layer, (0, 0))
        #god_rays.render_depth_map(shadow_casters)
        #screen.blit(god_rays.depth_map, (0, 0))

        # Post-Processing
        #shader_data = {'TIME': time}
        #god_rays.send_data_to_shader(shader_data)
        #god_rays.render()
        #screen.blit(sunshafts_layer, (0, 0))

        # Clearing
        clear_layer(ground_layer)
        clear_layer(objects_layer)
        shadows_layer.fill((1, 1, 1, 0))
        # Screen Rendering
        sc_shader.render()

        pygame.display.flip()

        clock.tick(FPS)
