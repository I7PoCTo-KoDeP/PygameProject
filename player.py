import pygame
from pygame.math import Vector2
from math import exp
from sprites import (player_group, all_sprites, player_image, shadow_casters, sort_by_y, save_group, decorations,
                     player_run)
from global_lightning import ShadowCaster
from help_functions import clamp, cut_sheet, collide
from constants import GLOBAL_LIGHTNING_ANGLE


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, casts_shadows=True):
        super().__init__(player_group, all_sprites, shadow_casters, sort_by_y, save_group)
        self.image = player_image
        self.size = player_image.get_width(), player_image.get_height()
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.collider = pygame.Rect(pos_x - 22, pos_y - 15, 36, 65)
        self.current_speed = 0
        self.sprite_y = self.image.get_rect().bottom
        self.flipped = False
        self.world_coordinates = [pos_x, pos_y]
        self.position = Vector2(pos_x, pos_y)
        self.run_frames = cut_sheet(player_run, 13, 1)
        self.idle_frames = player_image
        self.cur_frame = 0
        if casts_shadows:
            self.shadow_caster = ShadowCaster(self.image, GLOBAL_LIGHTNING_ANGLE)

    def flip(self):
        if not self.flipped:
            self.image = pygame.transform.flip(self.image, False, False)
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)

    def move(self, max_speed, acceleration, time):
        direction_x, direction_y = self.get_direction()

        if direction_x == 0 and direction_y == 0:
            self.stop(acceleration)
            self.image = self.idle_frames
            self.flip()
        if (direction_x != 0 or direction_y != 0) and int(time * 100) % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.run_frames)
            self.image = self.run_frames[self.cur_frame]
            self.flip()

        self.current_speed = self.calculate_speed(max_speed, 0.2, 2)
        self.rect.x += self.current_speed * direction_x
        self.rect.y += self.current_speed * direction_y
        self.world_coordinates[0] += self.current_speed * direction_x
        self.world_coordinates[1] += self.current_speed * direction_y
        self.collider.x += self.current_speed * direction_x
        self.collider.y += self.current_speed * direction_y
        for i in decorations:
            if collide(self.collider, i.collider):
                self.rect.x -= self.current_speed * direction_x
                self.rect.y -= self.current_speed * direction_y
                self.world_coordinates[0] -= self.current_speed * direction_x
                self.world_coordinates[1] -= self.current_speed * direction_y
                self.collider.x -= self.current_speed * direction_x
                self.collider.y -= self.current_speed * direction_y

        self.shadow_caster.setup_new_image(self.image)

    def calculate_speed(self, max_speed, smoothness, exp_pow=1):
        speed = clamp(0, max_speed, self.current_speed * exp(exp_pow) * smoothness)
        return speed

    def stop(self, acceleration):
        self.cur_frame = 0
        self.current_speed = acceleration

    def get_direction(self):
        direction = Vector2(0, 0)
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            direction.x = -1
            self.flipped = True
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            direction.x = 1
            self.flipped = False
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            direction.y = -1
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            direction.y = 1
        return direction

    def get_position(self):
        return self.world_coordinates

    def update(self):
        self.position = Vector2(self.rect.center)
        self.shadow_caster.cast_shadow(self.rect.x, self.rect.y)
