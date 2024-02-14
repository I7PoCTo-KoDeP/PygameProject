class Camera:
    def __init__(self, screen_size, offset):
        self.dx = 0
        self.dy = 0
        self.screen_size = screen_size
        self.offset = offset

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.screen_size[0] // 2 + self.offset[0])
        self.dy = -(target.rect.y + target.rect.h // 2 - self.screen_size[1] // 2 + self.offset[1])
