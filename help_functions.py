import pygame
import os
import sys
import json


def load_image(name, colorkey=None):                # Function which loads images.
    fullname = os.path.join('data/sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def cut_sheet(sheet, columns, rows):
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))
    return frames


def clamp(min_value, max_value, value):             # Function which returns "clamped" value
    if min_value <= value <= max_value:
        return value
    elif min_value > value:
        return min_value
    else:
        return max_value


def load_map(path):                                 # Function which loads level from .json
    with open(path, 'r', encoding='utf-8') as map_file:
        objects = []
        file = map_file.read()
        data = json.loads(file)
        for i in data:
            for j in i:
                obj = j['Class_name'] + '('
                args = []
                for key, val in j.items():
                    if key != 'Class_name':
                        args.append(key + '=' + str(val))
                obj += ', '.join(i for i in args) + ')'
                objects.append(obj)
        return objects


def play_music(path, loop, volume):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loop)
    pygame.mixer.music.set_volume(volume)


def terminate():
    pygame.quit()
    sys.exit()


def clear_layer(layer):
    layer.fill((255, 255, 255, 0))


def collide(rect1, rect2):
    if rect1.x == min(rect1.x, rect2.x):
        left = rect1.x
        width = rect1.w
    else:
        left = rect2.x
        width = rect2.w
    if rect1.y == min(rect1.y, rect2.y):
        bottom = rect1.y
        height = rect1.h
    else:
        bottom = rect2.y
        height = rect2.h
    if left + width > max(rect1.x, rect2.x) and bottom + height > max(rect1.y, rect2.y):
        return True
    return False
