from pygame.math import Vector2


class Camera:
    def __init__(self, screen_size, speed):
        self.position = Vector2(screen_size[0] // 2, screen_size[1] // 2)
        self.screen_size = screen_size
        self.speed = speed
        self.offset = Vector2(0, 0)

    def apply(self, obj):
        obj.rect.x += self.offset.x
        obj.rect.y += self.offset.y

    def update(self, target):
        heading = target.position - self.position
        self.position += heading * self.speed
        self.offset = (Vector2(self.screen_size[0] / 2, self.screen_size[1] / 2) - self.position) * self.speed

