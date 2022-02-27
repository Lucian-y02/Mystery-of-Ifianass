import threading
import time

import pygame

import constants


pygame.init()


# Базовая вертикальная стена
class VerticalWall(pygame.sprite.Sprite):
    def __init__(self, group, coordinates):
        super(VerticalWall, self).__init__(group)
        self.shift = constants.wall_shift
        self.image = pygame.Surface((1, 64 - self.shift * 2))
        self.image.fill((200, 204, 194))
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1] + self.shift


# Базовая горизонтальная стена
class HorizontalWall(pygame.sprite.Sprite):
    def __init__(self, group, coordinates):
        super(HorizontalWall, self).__init__(group)
        self.shift = constants.wall_shift
        self.image = pygame.Surface((64 - self.shift * 2, 1))
        self.image.fill((200, 204, 194))
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0] + self.shift
        self.rect.y = coordinates[1]


class Box:
    def __init__(self, group, x=0, y=0):
        HorizontalWall(group, (x, y - 1))
        HorizontalWall(group, (x, y + 64))
        VerticalWall(group, (x - 1, y))
        VerticalWall(group, (x + 64, y))


# Указатель
class Pointer(pygame.sprite.Sprite):
    def __init__(self, group, user, size=(16, 20)):
        super(Pointer, self).__init__(group)
        self.user = user

        # Смещение указателя
        self.shift_x = self.user.rect.x + self.user.rect.width // 2 - 8
        self.shift_y = self.user.rect.y + self.user.rect.height + 3

        self.image = pygame.Surface(size)
        self.image.fill((200, 204, 194))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = self.shift_x
        self.rect.y = self.shift_y

        self.side = "DOWN"

    def update(self):
        self.rect.x = self.shift_x
        self.rect.y = self.shift_y

    def side_update(self, side):
        self.side = side
        if side == "UP":
            self.shift_x = self.user.rect.x + self.user.rect.width // 2 - 8
            self.shift_y = self.user.rect.y - 6 - self.rect.height
        elif side == "DOWN":
            self.shift_x = self.user.rect.x + self.user.rect.width // 2 - 8
            self.shift_y = self.user.rect.y + self.user.rect.height + 6
        elif side == "LEFT":
            self.shift_x = self.user.rect.x - 6 - self.rect.width
            self.shift_y = self.user.rect.y + self.user.rect.height // 2 - self.rect.height // 2
        elif side == "RIGHT":
            self.shift_x = self.user.rect.x + self.user.rect.width + 6
            self.shift_y = self.user.rect.y + self.user.rect.height // 2 - self.rect.height // 2


# Удар
class Chop(pygame.sprite.Sprite):
    def __init__(self, group, user, life_time=0.25, damage=1):
        super(Chop, self).__init__(group)
        self.user = user

        self.image = pygame.Surface((52, 16))
        self.image.fill((200, 204, 194))
        self.rect = self.image.get_rect()

        # Характеристики
        self.life_time = life_time  # Продолжительность отображения удара
        self.shift = 4  # Смещение
        self.damage = damage  # Урон
        self.tangible = True  # Может нанести урок

        # Определение стороны удара и расчёт коориднат
        if user.pointer.side == "UP":
            self.rect.x = user.rect.x - (self.rect.width - user.rect.width) // 2
            self.rect.y = (user.pointer.rect.y -
                           (self.rect.height - user.pointer.rect.height) - self.shift)
        elif user.pointer.side == "DOWN":
            self.rect.x = user.rect.x - (self.rect.width - user.rect.width) // 2
            self.rect.y = user.pointer.rect.y + self.shift
        else:
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect()
            self.rect.y = (user.pointer.rect.y -
                           (self.rect.height - user.pointer.rect.height) // 2)
            if user.pointer.side == "RIGHT":
                self.rect.x = user.pointer.rect.x + self.shift
            else:
                self.rect.x = (user.pointer.rect.x +
                               user.pointer.rect.width - self.rect.width - self.shift)

        threading.Thread(target=self.life_timer).start()

    # Таймер, по истечению которого удар исчезнет
    def life_timer(self):
        time.sleep(self.life_time)
        self.user.speed = self.user.default_speed
        self.kill()


# Индикатор здоровья
class HealthPointsIndicator(pygame.sprite.Sprite):
    def __init__(self, group, user, **kwargs):
        super(HealthPointsIndicator, self).__init__(group)
        self.user = user

        self.shift_horizontal = kwargs.get("shift_horizontal", 0)
        self.shift_vertical = kwargs.get("shift_vertical", 6)

        self.image = pygame.Surface(kwargs.get("size", (64, 4)))
        self.image.fill(kwargs.get("color", (200, 204, 194)))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.x + self.shift_horizontal
        self.rect.y = self.rect.y + self.shift_vertical

        self.max_health_points = user.max_health_points

    def update(self):
        if self.user.health_points <= 0:
            self.kill()
        self.image = pygame.transform.scale(self.image,
                                            (max(int(self.rect.width *
                                                     (self.user.health_points /
                                                      self.max_health_points)), 0), 3))
        self.rect.x = self.user.rect.x - self.shift_horizontal
        self.rect.y = self.user.rect.y - self.shift_vertical
