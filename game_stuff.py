import threading
import time

import pygame

import constants


pygame.init()


# Базовая вертикальная стена
class VerticalWall(pygame.sprite.Sprite):
    def __init__(self, group, coord, **kwargs):
        super(VerticalWall, self).__init__(group)
        self.shift = kwargs.get("shift", constants.WALL_SHIFT)
        self.image = pygame.Surface(kwargs.get("size", (1, 64 - self.shift * 2)))
        self.image.fill((200, 204, 194))
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1] + self.shift


# Базовая горизонтальная стена
class HorizontalWall(pygame.sprite.Sprite):
    def __init__(self, group, coord, **kwargs):
        super(HorizontalWall, self).__init__(group)
        self.shift = kwargs.get("shift", constants.WALL_SHIFT)
        self.image = pygame.Surface(kwargs.get("size", (64 - self.shift * 2, 1)))
        self.image.fill((200, 204, 194))
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + self.shift
        self.rect.y = coord[1]


class Box:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] - 1))
        HorizontalWall(group, (coord[0], coord[1] + 64))
        VerticalWall(group, (coord[0] - 1, coord[1]))
        VerticalWall(group, (coord[0] + 64, coord[1]))


# Северная стена
class NorthWall:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] - 1))


# Южная стена
class SouthWall:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] + 64))


# Западная стена
class WesternWall:
    def __init__(self, group, coord):
        VerticalWall(group, (coord[0] - 1, coord[1]))


# Восточная стена
class EastWall:
    def __init__(self, group, coord):
        VerticalWall(group, (coord[0] + 64, coord[1]))


# Верхний левый угол
class TopLeftCorner:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] - 1))
        VerticalWall(group, (coord[0] - 1, coord[1]))


# Верхний правый угол
class TopRightCorner:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] - 1))
        VerticalWall(group, (coord[0] + 64, coord[1]))


# Нижний левый угол
class DownLeftCorner:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] + 64))
        VerticalWall(group, (coord[0] - 1, coord[1]))


# Нижний правый угол
class DownRightCorner:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] + 64))
        VerticalWall(group, (coord[0] + 64, coord[1]))


# Середина горизонтальной платформы в 1 блок
class MiddleHorizontalPlatform:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] - 1))
        HorizontalWall(group, (coord[0], coord[1] + 64))


# Западный конец горизонтальной платформы в 1 блок
class WesternHorizontalPlatform:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] - 1))
        HorizontalWall(group, (coord[0], coord[1] + 64))
        VerticalWall(group, (coord[0] - 1, coord[1]))


# Восточный конец горизонтальной платформы в 1 блок
class EastHorizontalPlatform:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] - 1))
        HorizontalWall(group, (coord[0], coord[1] + 64))
        VerticalWall(group, (coord[0] + 64, coord[1]))


# Середина вертикальной платформы в 1 блок
class MiddleVerticalPlatform:
    def __init__(self, group, coord):
        VerticalWall(group, (coord[0] - 1, coord[1]))
        VerticalWall(group, (coord[0] + 64, coord[1]))


# Северный конец горизонтальной платформы в 1 блок
class NorthVerticalPlatform:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] - 1))
        VerticalWall(group, (coord[0] - 1, coord[1]))
        VerticalWall(group, (coord[0] + 64, coord[1]))


# Южный конец горизонтальной платформы в 1 блок
class SouthVerticalPlatform:
    def __init__(self, group, coord):
        HorizontalWall(group, (coord[0], coord[1] + 64))
        VerticalWall(group, (coord[0] + 64, coord[1]))
        VerticalWall(group, (coord[0] - 1, coord[1]))


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
        print("ok")
        super(HealthPointsIndicator, self).__init__(group)
        self.user = user

        self.shift_horizontal = kwargs.get("shift_horizontal", 0)
        self.shift_vertical = kwargs.get("shift_vertical", -4)

        self.image = pygame.Surface(kwargs.get("size", (64, 4)))
        self.image.fill(kwargs.get("color", (200, 204, 194)))
        self.rect = self.image.get_rect()

        self.rect.x = self.user.rect.x + self.shift_horizontal
        self.rect.y = self.user.rect.y + self.shift_vertical - self.rect.height

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


# Зона поражения (пропасть, море и т.д.)
class KillZone(pygame.sprite.Sprite):
    def __init__(self, group, coord, **kwargs):
        super(KillZone, self).__init__(group)
        self.image = pygame.Surface(kwargs.get("size", (64, 64)))
        self.image.fill((150, 29, 31))
        self.image.set_alpha(50)
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + kwargs.get("shift_x", 0)
        self.rect.y = coord[1] + kwargs.get("shift_y", 0)


# Западная сторона зоны поражения
class WesternKillZone(KillZone):
    def __init__(self, group, coord):
        super(WesternKillZone, self).__init__(group, coord, size=(40, 64),
                                              shift_x=24)


# Восточная сторона зоны поражения
class EastKillZone(KillZone):
    def __init__(self, group, coord):
        super(EastKillZone, self).__init__(group, coord, size=(40, 64))


# Северная сторона зоны поражения
class NorthKillZone(KillZone):
    def __init__(self, group, coord):
        super(NorthKillZone, self).__init__(group, coord, size=(64, 40),
                                            shift_y=24)


# Южная сторона зоны поражения
class SouthKillZone(KillZone):
    def __init__(self, group, coord):
        super(SouthKillZone, self).__init__(group, coord, size=(64, 40))


# Верхний левый угол зоны поражения
class TopLeftKillZoneCorner(KillZone):
    def __init__(self, group, coord):
        super(TopLeftKillZoneCorner, self).__init__(group, coord, size=(40, 40),
                                                    shift_x=24, shift_y=24)


# Нижний левый угол зоны поражения
class DownLeftKillZoneCorner(KillZone):
    def __init__(self, group, coord):
        super(DownLeftKillZoneCorner, self).__init__(group, coord, size=(40, 40),
                                                     shift_x=24)


# Верхний правый угол зоны поражения
class TopRightKillZoneCorner(KillZone):
    def __init__(self, group, coord):
        super(TopRightKillZoneCorner, self).__init__(group, coord, size=(40, 40),
                                                     shift_y=24)


# Нижний правый угол зоны поражения
class DownRightKillZoneCorner(KillZone):
    def __init__(self, group, coord):
        super(DownRightKillZoneCorner, self).__init__(group, coord, size=(40, 40))


class VerticalSingleKillZone(KillZone):
    def __init__(self, group, coord):
        super(VerticalSingleKillZone, self).__init__(group, coord, size=(16, 64),
                                                     shift_x=24)


class HorizontalSingleKillZone(KillZone):
    def __init__(self, group, coord):
        super(HorizontalSingleKillZone, self).__init__(group, coord, size=(64, 16),
                                                       shift_y=24)


class SingleKillZoneCorner(KillZone):
    def __init__(self, group, coord):
        super(SingleKillZoneCorner, self).__init__(group, coord, size=(16, 16),
                                                   shift_x=24, shift_y=24)


# Передвижной объект
class MobileObject(pygame.sprite.Sprite):
    def __init__(self, groups: dict, coord, **kwargs):
        super(MobileObject, self).__init__(groups["game_stuff"])
        self.shift = kwargs.get("shift", constants.WALL_SHIFT)
        self.image = pygame.Surface(kwargs.get("size", (32, 32)))
        self.image.fill((27, 29, 100))
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + (64 - self.rect.width) // 2
        self.rect.y = coord[1] + (64 - self.rect.height) // 2

        self.groups_data = groups

    def update(self):
        self.check_collision()

    def check_collision(self):
        # Столкновение со стенами
        for wall in self.groups_data["walls"]:
            if (self.rect.colliderect(wall.rect) and
                    wall.__class__.__name__ == "HorizontalWall"):
                pass
            if (self.rect.colliderect(wall.rect) and
                    wall.__class__.__name__ == "VerticalWall"):
                pass

        # Столкновение с другими игровыми объектами
        for obj in self.groups_data["game_stuff"]:
            if (self.rect.colliderect(obj.rect) and
                    obj.__class__.__name__ == "KillZone"):
                self.kill()
