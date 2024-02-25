import pygame
from initialization import scale
from help_functions import clamp


class UIElements:
    def __init__(self, position, surface):
        self.position = position
        self.surface = surface
        self.active = False

    def set_active(self, state):
        self.active = True
        if state:
            self.render()

    def on_click(self):
        pass

    def render(self):
        pass


class Button(UIElements):
    def __init__(self, position, button_size, on_click_event, surface, text, image=None):
        super().__init__(position, surface)
        self.rect = pygame.Rect(position[0] * scale, position[1] * scale, button_size[0] * scale,
                                button_size[1] * scale)
        self.size = button_size
        self.on_click_event = on_click_event
        self.text = text
        self.image = image

        self.render()

    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and self.active:
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


class Slider(UIElements):
    def __init__(self, position, handle_diameter, width, height, surface, value, slider_image=None, handle_image=None):
        super().__init__(position, surface)
        self.background_rect = pygame.Rect(position[0] * scale, position[1] * scale, (position[0] + width) * scale,
                                           (position[1] + height) * scale)
        self.radius = handle_diameter / 2
        self.width = width
        self.height = height
        self.slider_img = slider_image
        self.handle_img = handle_image
        self.value = value.get()
        self.slider = pygame.Surface((self.width + handle_diameter, self.radius * 2), pygame.SRCALPHA)
        self.changed_value = value

        self.render()

    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.background_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and self.active:
            x = mouse_pos[0] / scale - self.position[0]
            self.value = clamp(0.0, 1.0, x / self.width)
            self.render()
            self.changed_value.set(self.value)

    def render(self):
        self.slider.fill((0, 0, 0))
        background = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        handle = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        background.fill((255, 255, 255))
        pygame.draw.circle(handle, (200, 200, 200), (self.radius, self.radius), self.radius)
        self.slider.blit(background, (self.radius, (2 * self.radius - self.height) / scale))
        self.slider.blit(handle, (clamp(0, self.width, self.width * self.value), 0))
        self.surface.blit(self.slider, self.position)
