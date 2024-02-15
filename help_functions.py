import pygame
import os
import sys
import json


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


def clamp(min_value, max_value, value):
    if min_value <= value <= max_value:
        return value
    elif min_value > value:
        return min_value
    else:
        return max_value


def load_map(path):
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


def terminate():
    pygame.quit()
    sys.exit()


def clear_layer(layer):
    layer.fill((255, 255, 255, 0))
