import pygame
import sys
from opengl_render_pipeline import OpenGLRenderPipeline


scale = 2
size = width, height = 640, 360
pipeline = OpenGLRenderPipeline(size, scale=scale)
screen = pipeline.get_screen()
screen.set_alpha(None)

shadows_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
ground_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
objects_layer = pygame.Surface(size, pygame.SRCALPHA, 32)
light_layer = pygame.Surface(size, pygame.SRCALPHA, 32)

get_trace = getattr(sys, 'gettrace', None)
dev_mode = False
if get_trace():
    dev_mode = True
show_fps = True
