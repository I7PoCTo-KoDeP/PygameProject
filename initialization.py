import pygame
from opengl_render_pipeline import OpenGLRenderPipeline


scale = 2
size = width, height = 640, 360
pipeline = OpenGLRenderPipeline(size, scale=scale)
screen = pipeline.get_screen()
dev_mode = True

shadows_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
ground_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
objects_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
sunshafts_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
