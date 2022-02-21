import pygame


pygame.init()


# Базовая вертикальная стена
class VerticalWall(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super(VerticalWall, self).__init__(group)
        self.image = pygame.Surface((1, 64))
        self.image.fill((200, 204, 194))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Базовая горизонтальная стена
class HorizontalWall(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super(HorizontalWall, self).__init__(group)
        self.image = pygame.Surface((64, 1))
        self.image.fill((200, 204, 194))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Box:
    def __init__(self, group, x, y):
        HorizontalWall(group, x, y - 1)
        HorizontalWall(group, x, y + 64)
        VerticalWall(group, x - 1, y)
        VerticalWall(group, x + 64, y)
