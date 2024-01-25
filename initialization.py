import pygame
from opengl_render_pipeline import OpenGLRenderPipeline


size = width, height = 640, 360
pipeline = OpenGLRenderPipeline(size, scale=2)
screen = pipeline.get_screen()
shadows_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
ground_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
decoration_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
sunshafts_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
