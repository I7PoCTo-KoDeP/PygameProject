import moderngl
import pygame


class OpenGLRenderPipeline:
    def __init__(self):
        self.ctx = moderngl.create_context()
