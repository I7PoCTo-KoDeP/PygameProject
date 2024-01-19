import moderngl
import pygame


class OpenGLRenderPipeline:
    def __init__(self):
        pygame.init()
        self.ctx = moderngl.create_context()

    def screen_initialization(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.Surface((width, height))
        return self.display

    def render_texture(self, render_obj, surf):
        framebuffer = self.ctx.simple_framebuffer(surf.get_size(), 4)
        scope = self.ctx.scope(framebuffer)
        with scope:
            framebuffer.use()
            render_obj.render(mode=moderngl.TRIANGLE_STRIP)
            surface = pygame.image.frombuffer(framebuffer.read(), surf.get_size(), 'RGB')
        scope.release()
        return surface

    class Shader:
        def __init__(self, vertex_shader='', fragment_shader=''):
            self.ctx = moderngl.create_context()

        def surface_to_texture(self, surface):
            self.texture = self.ctx.texture(surface.get_size(), 4)
            self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
            self.texture.swizzle = 'BGRA'
            self.texture.write(surface.get_view('1'))


def file_reader(path):
    with open(path, mode='r', encoding='utf-8') as f:
        shader = f.read()
    return shader

