import pygame
import sys
from opengl_render_pipeline import OpenGLRenderPipeline


scale = 2
size = width, height = 640, 360
pipeline = OpenGLRenderPipeline(size, scale=scale)
screen = pipeline.get_screen()

shadows_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
ground_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
objects_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
sunshafts_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
light_layer = pygame.Surface(size, pygame.SRCALPHA, 32)

gettrace = getattr(sys, 'gettrace', None)
dev_mode = False
if gettrace():
    dev_mode = True
