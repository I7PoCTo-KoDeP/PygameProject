from opengl_render_pipeline import PostProcessing
from initialization import *
from sprites import all_sprites, tiles_group, sort_by_y, shadow_casters, save_group, decorations, light_sources
from constants import *
from player import Player
from camera import Camera
from global_lightning import GodRays
from save_module import save, load_save
from help_functions import clear_layer, load_map, play_music
from start_screen import StartScreen
from point_light import PointLight
from scene_objects import Tile, Decoration


sc_shader = PostProcessing(size, screen, 'shaders/Screen.vert', 'shaders/Screen.frag')
god_rays = GodRays(GLOBAL_LIGHTNING_ANGLE, (250, 250, 210), 10)
camera = Camera(size, 0.2)
time = 0


if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()

    start_screen = StartScreen(clock, with_splash=True)

    objects = load_map('maps/game_map.json')
    for i in objects:
        eval(i)

    save_data = load_save()
    if save_data is not None:
        player = eval(save_data[0])
    else:
        player = Player(0, 0)

    god_rays.create_god_rays(shadow_casters)

    play_music('data/music/let-go.mp3', -1, MASTER_VOLUME.get())

    while running:
        time += 0.01
        clear_layer(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    save(save_group)
                    main_menu = StartScreen(clock)
                    play_music('data/music/let-go.mp3', -1, MASTER_VOLUME.get())
                if pygame.key.get_pressed()[pygame.K_F11]:
                    pipeline.change_scale(3)

        player.move(PLAYER_MAX_SPEED, PLAYER_START_SPEED, time)

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        all_sprites.update()

        for i in light_sources:
            i.render()

        # Frame Formation
        tiles_group.draw(screen)
        screen.blit(shadows_layer, (0, 0))
        sort_by_y.draw(screen)
        # light_sources.draw(light_layer)
        #screen.blit(ground_layer, (0, 0))
        #screen.blit(objects_layer, (0, 0))
        # screen.blit(light_layer, (0, 0))

        # Visualise colliders and show FPS
        if show_fps:
            font = pygame.font.Font(None, 20)
            fps = font.render(str(round(clock.get_fps())), True, (0, 0, 0))
            screen.blit(fps, (size[0] - 30, 10))
        if dev_mode:
            font = pygame.font.Font(None, 20)
            fps = font.render(str(round(clock.get_fps())), True, (0, 0, 0))
            screen.blit(fps, (size[0] - 30, 10))
            pygame.draw.rect(screen, (0, 128, 0), player.collider, width=2)
            for i in decorations:
                pygame.draw.rect(screen, (0, 128, 0), i.collider, width=2)

        # Post-Processing
        shader_data = {'time': time}
        god_rays.send_data_to_shader(shader_data)
        god_rays.render()
        screen.blit(god_rays.god_rays, (0, 0))

        # Clearing
        clear_layer(light_layer)
        shadows_layer.fill((0, 0, 0, 0))

        # Screen Rendering
        sc_shader.render()
        pygame.display.flip()
        clock.tick(FPS)
