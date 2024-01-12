import pygame
import pygame_shaders


pygame.init()
size = width, height = 320 * 4, 180 * 4

screen = pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface(size)
