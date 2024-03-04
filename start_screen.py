import pygame

from constants import FPS, MASTER_VOLUME
from initialization import screen, size
from help_functions import load_image, terminate, play_music
from opengl_render_pipeline import PostProcessing
from UI_elements import Button, Slider


screen_shader = PostProcessing(size, screen, 'shaders/Screen.vert', 'shaders/Screen.frag')


class StartScreen:
    """Manager class"""
    def __init__(self, clock, with_splash=False):
        self.main_menu = MainMenu(self)
        self.settings = SettingsMenu(self)
        self.with_splash = with_splash
        self.clock = clock
        self.start_screen()

    def start_screen(self):
        if self.with_splash:
            splash_screen()
            pygame.time.delay(1000)
        self.main_menu.render()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pass
                if self.main_menu.started:
                    pygame.mixer.music.pause()
                    return
            for i in self.main_menu.main_menu_GUI:
                i.on_click()
            for i in self.settings.settings_GUI:
                i.on_click()

            pygame.mixer.music.set_volume(MASTER_VOLUME.get())

            screen_shader.render()
            pygame.display.flip()
            self.clock.tick(FPS)

    def to_settings(self):
        for i in self.main_menu.main_menu_GUI:
            i.set_active(False)
        screen.fill((31, 206, 203))
        self.settings.render()

    def to_main_menu(self):
        for i in self.settings.settings_GUI:
            i.set_active(False)
        screen.fill((31, 206, 203))
        self.main_menu.render()


class MainMenu:
    def __init__(self, manager):
        self.main_menu_GUI = []
        self.channel = None
        self.started = False
        self.manager = manager
        self.init_main_menu()

    def init_main_menu(self):
        # Main menu music
        play_music('data/music/forest-queen-tale.mp3', -1, MASTER_VOLUME.get())
        # Creating Buttons
        start_button = Button((10, size[1] // 3), (90, 30), self.start, screen, 'Play')
        settings_button = Button((10, size[1] // 3 + 40), (90, 30), self.manager.to_settings, screen, 'Settings')
        exit_button = Button((10, size[1] // 3 + 80), (90, 30), terminate, screen, 'Exit')
        self.main_menu_GUI.append(start_button)
        self.main_menu_GUI.append(settings_button)
        self.main_menu_GUI.append(exit_button)

    def render(self):
        background = load_image('Background.png')
        screen.fill((31, 206, 203))
        font = pygame.font.Font('data/fonts/agsfontsetserif1.ttf', 48)
        string_rendered = font.render('The Last Traveler', 1, pygame.Color('white'))
        screen.blit(background, (0, 0))
        screen.blit(string_rendered, (10, 10))
        for i in self.main_menu_GUI:
            i.set_active(True)

    def start(self):
        self.started = True


class SettingsMenu:
    def __init__(self, manager):
        self.settings_GUI = []
        self.sliders = []
        self.manager = manager
        self.init_settings()

    def init_settings(self):
        back_button = Button((10, size[1] - 40), (90, 30), self.manager.to_main_menu, screen, 'Back')
        volume_slider = Slider((170, 20), 12, 120, 8, screen, MASTER_VOLUME)
        self.settings_GUI.append(back_button)
        self.settings_GUI.append(volume_slider)

    def render(self):
        font = pygame.font.Font('data/fonts/agsfontsetserif1.ttf', 24)
        string_rendered = font.render('Master volume', 1, pygame.Color('black'))
        screen.blit(string_rendered, (10, 10))
        for i in self.settings_GUI:
            i.set_active(True)


def splash_screen():
    screen.fill((27, 1, 44))
    intro_text = 'NightStormStudios'
    font = pygame.font.Font('data/fonts/agsfontsetserif1.ttf', 36)
    string_rendered = font.render(intro_text, 1, (255, 207, 64))
    text_size = string_rendered.get_rect().size
    position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
    screen.blit(string_rendered, position)
    screen_shader.render()
    pygame.display.flip()
