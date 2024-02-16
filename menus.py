import pygame

from constants import FPS
from initialization import screen, size, scale
from help_functions import load_image, terminate
from opengl_render_pipeline import PostProcessing


class MainMenu:
    def __init__(self, clock, splash_screen):
        self.clock = clock
        self.started = False
        self.buttons = []
        self.screen_shader = PostProcessing(size, screen, 'shaders/Screen.vert', 'shaders/Screen.frag')
        self.with_splash = splash_screen
        self.main_loop()

    def main_loop(self):
        if self.with_splash:
            self.splash_screen()
            pygame.time.delay(1000)
        self.main_menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pass
                if self.started:
                    return

            for i in self.buttons:
                i.click()
            self.screen_shader.render()
            pygame.display.flip()
            self.clock.tick(FPS)

    def splash_screen(self):
        screen.fill((27, 1, 44))
        intro_text = 'NightStormStudios'
        font = pygame.font.Font('data/fonts/agsfontsetserif1.ttf', 36)
        string_rendered = font.render(intro_text, 1, (255, 207, 64))
        text_size = string_rendered.get_rect().size
        position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
        screen.blit(string_rendered, position)
        self.screen_shader.render()
        pygame.display.flip()

    def main_menu(self):
        screen.fill((31, 206, 203))
        font = pygame.font.Font('data/fonts/agsfontsetserif1.ttf', 48)
        string_rendered = font.render('The Last Traveler', 1, pygame.Color('black'))
        screen.blit(string_rendered, (10, 10))
        start_button = Button((10, size[1] // 3), (90, 30), self.start, screen, 'Play')
        start_button.render()
        self.buttons.append(start_button)
        settings_button = Button((10, size[1] // 3 + 40), (90, 30), self.settings, screen, 'Settings')
        settings_button.render()
        self.buttons.append(settings_button)
        exit_button = Button((10, size[1] // 3 + 80), (90, 30), terminate, screen, 'Exit')
        exit_button.render()
        self.buttons.append(exit_button)

    def settings(self):
        print('Whoops. It`s unaviable now.')

    def start(self):
        self.started = True


class Button:
    def __init__(self, position, button_size, on_click_event, surface, text, image=None):
        self.position = position
        self.size = button_size
        self.surface = surface
        self.rect = pygame.Rect(position[0] * scale, position[1] * scale, button_size[0]* scale, button_size[1] * scale)
        self.on_click_event = on_click_event
        self.text = text

    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.on_click_event()

    def render(self):
        button = pygame.Surface(self.size)
        button.fill((255, 255, 255))
        font = pygame.font.Font('data/fonts/agsfontsetserif1.ttf', 24)
        string_rendered = font.render(self.text, 1, pygame.Color('black'))
        x = (button.get_width() - string_rendered.get_rect().size[0]) // 2
        y = (button.get_height() - string_rendered.get_rect().size[1]) // 2
        button.blit(string_rendered, (x, y))
        self.surface.blit(button, self.position)


class Slider:
    def __init__(self):
        pass
