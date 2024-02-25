from array import array
import moderngl
import pygame


class OpenGLRenderPipeline:
    """Creates RenderPipeline"""
    def __init__(self, size, scale=1):
        pygame.init()
        self.screen_size = size[0] * scale, size[1] * scale
        self.screen = pygame.display.set_mode(self.screen_size, pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.Surface(size)
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = self.ctx.SRC_ALPHA, self.ctx.ONE_MINUS_SRC_ALPHA

    def get_screen(self) -> pygame.Surface:
        """Returns screen where you can draw."""
        return self.display

    def get_screen_texture(self):
        return self.screen

    def create_texture(self, surface: pygame.Surface) -> moderngl.Texture:
        """Create texture from pygame surface"""
        return surface_to_texture(self.ctx, surface)


class Shader:
    """Create shader"""
    def __init__(self, vertex_shader='', fragment_shader='', sprite=None, size=None, data=None):
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
        if sprite is not None:
            self.img = sprite
            self.framebuffer = self.ctx.simple_framebuffer(self.img.get_size(), 4)
            self.texture = surface_to_texture(self.ctx, self.img)
        else:
            self.framebuffer = self.ctx.simple_framebuffer(size, 4)
        self.program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.render_object = self.ctx.vertex_array(self.program,
                                                   [(self.quad_buffer, '2f 2f', 'vertexPos', 'vertexTexCoord')])
        self.shader_data = data

    def send_data(self):
        if self.shader_data is not None:
            for key, val in self.shader_data.items():
                self.program[key] = val

    def render(self, image=None, create_texture=False) -> pygame.Surface:
        """Renders texture and returns pygame.Surface"""
        if image is not None:
            self.img = image
        if create_texture:
            self.texture = surface_to_texture(self.ctx, self.img)
        self.texture.use()
        self.send_data()
        scope = self.ctx.scope(self.framebuffer)
        with scope:
            self.framebuffer.use()
            self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
            surface = pygame.image.frombuffer(self.framebuffer.read(components=4), self.img.get_size(), 'RGBA')
        scope.release()
        self.texture.release()
        return surface

    def blit_image(self, img, pos):
        self.img.fill((0, 0, 0, 0))
        self.img.blit(img, pos)


class PostProcessing:
    """Class for post-processing. Shader for screen."""
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
