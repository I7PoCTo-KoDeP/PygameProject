import pygame
from opengl_render_pipeline import OpenGLRenderPipeline


size = width, height = 320 * 4, 180 * 4
pipeline = OpenGLRenderPipeline(size)
screen = pipeline.get_screen()
shadows_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
ground_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
decoration_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
sunshafts_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
