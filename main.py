import pygame
import moderngl
from array import array

from initialization import screen, display, size
from sprites import all_sprites, player_group
from constants import X_OFFSET, FPS
from player import Player
from scene_objects import Decoration, Tile


ctx = moderngl.create_context()

fbo = ctx.framebuffer(ctx.renderbuffer(size), ctx.depth_renderbuffer(size))

quad_buffer = ctx.buffer(data=array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0
]))

vert_shader = '''#version 330 core

layout (location=0) in vec2 vertexPos;
layout (location=1) in vec2 vertexTexCoord;

out vec2 uv;

void main()
{
    gl_Position = vec4(vertexPos, 0.0, 1.0);
    uv = vertexTexCoord;
}
'''

frag_shader = '''#version 330 core

in vec2 uv;

out vec4 color;

uniform sampler2D tex;

void main()
{
        color = vec4(texture(tex, uv).rgb, 1.0);
}
'''

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vertexPos', 'vertexTexCoord')])


def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex


def load_field(rows, columns):
    tiles = []
    for i in range(-1, rows):
        for j in range(-1, columns):
            if j % 2 == 0:
                color = 'white'
                offset = X_OFFSET
            else:
                color = 'black'
                offset = 0
            tile = Tile(color, i, j, offset)
            tiles.append(tile)


if __name__ == '__main__':
    running = True
    clock = pygame.time.Clock()

    load_field(20, 20)
    block = Decoration('block', 99, 114)
    block1 = Decoration('block', 159, 144)
    wall = Decoration('stone_wall', 259, 59)
    player = Player(100, 100)

    while running:
        display.fill(pygame.Color('white'))

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            player.move(-1, 0)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            player.move(1, 0)
        if pygame.key.get_pressed()[pygame.K_UP]:
            player.move(0, -1)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            player.move(0, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pass

        all_sprites.draw(display)
        all_sprites.update()

        frame_tex = surf_to_texture(display)
        frame_tex.use()
        render_object.render(mode=moderngl.TRIANGLE_STRIP)

        pygame.display.flip()

        frame_tex.release()

        clock.tick(FPS)
