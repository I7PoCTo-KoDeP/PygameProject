from array import array
import moderngl
import pygame


class OpenGLRenderPipeline:
    def __init__(self, screen_size):
        pygame.init()
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size, pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.Surface(screen_size)

    def get_screen(self):
        return self.display


class Shader:
    def __init__(self, sprite, vertex_shader='', fragment_shader='', data=None):
        vertex_shader = file_reader(vertex_shader)
        fragment_shader = file_reader(fragment_shader)
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = self.ctx.SRC_ALPHA, self.ctx.ONE_MINUS_SRC_ALPHA
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, -1.0, 0.0, 0.0,
            1.0, -1.0, 1.0, 0.0,
            -1.0, 1.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 1.0
        ]))
        self.texture = surface_to_texture(self.ctx, sprite)
        self.program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.render_object = self.ctx.vertex_array(self.program,
                                                   [(self.quad_buffer, '2f 2f', 'vertexPos', 'vertexTexCoord')])
        self.img = sprite
        self.shader_data = data

    def send_data(self):
        if self.shader_data is not None:
            for key, val in self.shader_data.items():
                self.program[key] = val

    def render(self):
        self.texture.use()
        self.send_data()
        framebuffer = self.ctx.simple_framebuffer(self.img.get_size(), 4)
        scope = self.ctx.scope(framebuffer)
        with scope:
            framebuffer.use()
            self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
            surface = pygame.image.frombuffer(framebuffer.read(), self.img.get_size(), 'RGB')
        scope.release()
        return surface


class PostProcessing:
    def __init__(self, screen_size, display, vertex_shader='', fragment_shader=''):
        vertex_shader = file_reader(vertex_shader)
        fragment_shader = file_reader(fragment_shader)

        self.ctx = moderngl.create_context()
        self.fbo = self.ctx.framebuffer(self.ctx.renderbuffer(screen_size),
                                        self.ctx.depth_renderbuffer(screen_size))
        self.quad_buffer = self.ctx.buffer(data=array('f', [
                -1.0, 1.0, 0.0, 0.0,
                1.0, 1.0, 1.0, 0.0,
                -1.0, -1.0, 0.0, 1.0,
                1.0, -1.0, 1.0, 1.0
            ]))
        self.program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.render_object = self.ctx.vertex_array(self.program,
                                                   [(self.quad_buffer, '2f 2f', 'vertexPos', 'vertexTexCoord')])
        self.display = display

    def render(self):
        screen_texture = surface_to_texture(self.ctx, self.display)
        screen_texture.use()
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        screen_texture.release()


def surface_to_texture(ctx, surface):
    texture = ctx.texture(surface.get_size(), 4)
    texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
    texture.swizzle = 'BGRA'
    texture.write(surface.get_view('1'))
    return texture


def file_reader(path):
    with open(path, mode='r', encoding='utf-8') as f:
        shader = f.read()
    return shader
