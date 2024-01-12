import pygame
import moderngl
from array import array

import pygame_shaders

from initialization import display, screen


ctx = moderngl.create_context()
quad_buffer = ctx.buffer(data=array('f', [
    -1.0, -1.0, 0.0, 0.0,
    1.0, -1.0, 1.0, 0.0,
    -1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0
]))


def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex


def file_reader(path):
    with open(path, mode='r', encoding='utf-8') as f:
        shader = f.read()
    return shader


vert_shader = file_reader('shaders/vertex.glsl')
frag_shader = file_reader('shaders/fragment.glsl')

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vertexPos', 'vertexTexCoord')])


def render_tex(render_obj, surf):
    framebuffer = ctx.simple_framebuffer(surf.get_size(), 4)
    scope = ctx.scope(framebuffer)
    with scope:
        framebuffer.use()
        render_obj.render(mode=moderngl.TRIANGLE_STRIP)
        surface = pygame.image.frombuffer(framebuffer.read(), surf.get_size(), 'RGB')
    scope.release()
    return surface


class ShadowCaster:
    @staticmethod
    def make_shadow(image, angle):
        # shader = pygame_shaders.Shader('shaders/vertex.glsl','shaders/fragment.glsl', image)
        image_res = pygame.Surface((image.get_height() * 2, image.get_width() * 2))
        image_res.blit(image, image.get_size())
        frame_tex = surf_to_texture(image_res)
        render_object.render(mode=moderngl.TRIANGLE_STRIP)
        frame_tex.use()
        program['imageTexture'] = angle

        img = render_tex(render_object, image_res)
        # img = shader.render()
        img.set_colorkey((0, 0, 0))

        pattern = pygame.Surface(image_res.get_size())
        pattern.fill((1, 1, 1))

        img.blit(pattern, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        img.set_alpha(100)
        img = pygame.transform.flip(img, False, True)

        return img

    def __init__(self, image):
        self.shadow = self.make_shadow(image, 340)

    def cast_shadow(self, pos_x, pos_y):
        display.blit(self.shadow, (pos_x, pos_y))
