import threading
import time

import pygame

from game_stuff import *
import constants


pygame.init()


# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self, groups: dict, coord, **kwargs):
        super(Player, self).__init__(groups["player"])
        self.groups_data = groups
        self.image = pygame.Surface((44, 64))
        self.image.fill((200, 204, 194))
        # Основной Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + 12
        self.rect.y = coord[1]
        # Rectangle для считывания столкновений со стенами
        self.collision_rect = pygame.rect.Rect(
            (self.rect.x, self.rect.y + self.rect.height - self.rect.width,
             self.rect.width, self.rect.width))  # 44 x 44

        # Геймпад
        self.game_pad = None
        try:
            self.game_pad = pygame.joystick.Joystick(0)
        except pygame.error:
            pass

        # Характеристики
        self.default_speed = constants.PLAYER_SPEED
        self.speed = self.default_speed
        self.respawn_coord = coord
        self.max_health_points = constants.PLAYER_MAX_HEALTH_POINTS
        self.health_points = kwargs.get("health_points", self.max_health_points)

        self.health_indicator = HealthIndicatorUi(self.groups_data["ui"], (32, 32),
                                                  user=self)

        # Перемещение
        self.move_x = 0
        self.move_y = 0

        # Управление
        self.control_data = {
            "keyboard": self.keyboard_check_pressing,
            "game_pad": self.game_pad_check_pressing
        }
        self.control_function = self.control_data[kwargs.get("control_function", "game_pad")]

        # Указатель
        self.pointer = Pointer(self.groups_data["game_stuff"], self)  # Указатель

        # Атака
        self.chop_cool_down = kwargs.get("shop_cool_down", 1)
        self.chop_ready = True  # Возможность провести атаку
        self.do_chop = False  # Атака

        # Рывок
        self.dash_cool_down = kwargs.get("dash_cool_down", 0.5)
        self.dash_ready = True  # Возможность сделать рывок
        self.do_dash = False  # Рывок
        self.dash_duration = kwargs.get("dash_duration", 0.4)  # Время продолжительности рывка

    def update(self):
        self.move_x = 0
        self.move_y = 0

        # Ослеживание нажатий
        self.control_function()

        # Рывок
        if self.do_dash:
            self.pointer.side_update(self.pointer.side)
            self.chop_ready = False
            if self.pointer.side == "UP":
                self.move_y -= self.default_speed * 2
            elif self.pointer.side == "DOWN":
                self.move_y += self.default_speed * 2
            elif self.pointer.side == "LEFT":
                self.move_x -= self.default_speed * 2
            elif self.pointer.side == "RIGHT":
                self.move_x += self.default_speed * 2

        # Смещение игрока
        self.rect.move_ip(self.move_x, self.move_y)
        self.collision_rect.x = self.rect.x
        self.collision_rect.y = self.rect.y + self.rect.height - self.rect.width

        # Отслеживание столкновений
        self.check_collision()

        if self.health_points <= 0:
            self.revival()

    # Управление клавиатурой
    def keyboard_check_pressing(self):
        key = pygame.key.get_pressed()

        # Вверх
        if (key[pygame.K_w] or key[pygame.K_UP]) and self.speed:
            self.move_y -= self.speed
            self.pointer.side_update("UP")
        # Вниз
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.speed:
            self.move_y += self.speed
            self.pointer.side_update("DOWN")
        # Вправо
        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.speed:
            self.move_x += self.speed
            self.pointer.side_update("RIGHT")
        # Влево
        if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.speed:
            self.move_x -= self.speed
            self.pointer.side_update("LEFT")
        # Удар
        if key[pygame.K_j] and self.chop_ready and not self.do_dash and not self.do_chop:
            Chop(self.groups_data["player_chops"], self, damage=60)
            self.speed = 0
            self.chop_ready = False
            self.do_chop = True
            threading.Thread(target=self.chop_timer_reloading).start()
        # Рывок
        if key[pygame.K_k] and self.dash_ready and not self.do_dash:
            threading.Thread(target=self.dash_timer).start()

    # Управление геймпадом
    def game_pad_check_pressing(self):
        increase_x = increase_y = 0  # Увеличение move_x и move_y
        if abs(self.game_pad.get_axis(0)) > 0.1:
            increase_x = self.speed * round(self.game_pad.get_axis(0))
        if abs(self.game_pad.get_axis(1)) > 0.1:
            increase_y = self.speed * round(self.game_pad.get_axis(1))
        elif abs(self.game_pad.get_hat(0)[0]) or abs(self.game_pad.get_hat(0)[1]):
            increase_x = self.speed * self.game_pad.get_hat(0)[0]
            increase_y = self.speed * self.game_pad.get_hat(0)[1] * -1
        if increase_x:
            self.move_x += (min(increase_x, -self.speed) if increase_x < 0 else
                            max(increase_x, self.speed))
            self.pointer.side_update("RIGHT" if increase_x > 0 else "LEFT")
        if increase_y:
            self.move_y += (min(increase_y, -self.speed) if increase_y < 0 else
                            max(increase_y, self.speed))
            self.pointer.side_update("DOWN" if increase_y > 0 else "UP")
        # Удар
        if (self.game_pad.get_button(2) and self.chop_ready
                and not self.do_dash and not self.do_chop):
            Chop(self.groups_data["player_chops"], self, damage=60)
            self.speed = 0
            self.chop_ready = False
            self.do_chop = True
            threading.Thread(target=self.chop_timer_reloading).start()
        # Рывок
        if self.game_pad.get_button(0) and self.dash_ready and not self.do_dash:
            threading.Thread(target=self.dash_timer).start()

    # Столкновения
    def check_collision(self):
        collision_vertical_wall = False
        collision_horizontal_wall = False
        obj_x = None
        obj_y = None
        # Столкновение со стенами
        for obj in self.groups_data["walls"]:
            if (self.collision_rect.colliderect(obj.rect) and
                    obj.__class__.__name__ == "VerticalWall"):
                collision_vertical_wall = True
                obj_x = obj.rect.x
            if (self.collision_rect.colliderect(obj.rect) and
                    obj.__class__.__name__ == "HorizontalWall"):
                collision_horizontal_wall = True
                obj_y = obj.rect.y

        # Столкновение с зонами поражения
        if (pygame.sprite.spritecollideany(self, self.groups_data["kill_zones"]) and
                not self.do_dash):
            self.revival()

        # Столкновение с другими игровыми объектами
        for obj in self.groups_data["game_stuff"]:
            if (self.collision_rect.colliderect(obj.rect) and
                    obj.__class__.__name__ == "Bullet"):
                obj.kill()
                self.health_points -= obj.damage

        # Столкновение со стенами
        if collision_vertical_wall:
            self.do_dash = False
            if (abs(self.collision_rect.x + self.collision_rect.width - obj_x) >
                    abs(self.collision_rect.x - obj_x)):
                self.rect.x += self.default_speed
            else:
                self.rect.x -= self.default_speed
            self.move_x = 0
        if collision_horizontal_wall:
            self.do_dash = False
            if (abs(self.collision_rect.y - obj_y) >
                    abs(self.collision_rect.y + self.collision_rect.height - obj_y)):
                self.rect.y -= self.default_speed
            else:
                self.rect.y += self.default_speed
            self.move_y = 0

    # Таймер, по истечению которого можно провести следующую атаку
    def chop_timer_reloading(self):
        time.sleep(self.chop_cool_down)
        self.chop_ready = True
        self.do_chop = False

    # Таймер, по истечению которого можно использовать рываок
    def dash_timer_reloading(self):
        time.sleep(self.dash_cool_down)
        self.dash_ready = True

    # Таймер, по истечению которого рывок заканчивается
    def dash_timer(self):
        self.groups_data["player_chops"].remove(self.groups_data["player_chops"])
        self.dash_ready = False
        self.do_dash = True
        self.speed = 0
        self.do_chop = False
        self.chop_ready = False
        time.sleep(self.dash_duration)
        self.do_dash = False
        self.speed = self.default_speed
        threading.Thread(target=self.dash_timer_reloading).start()
        time.sleep(0.5)
        self.pointer.side_update(self.pointer.side)
        self.groups_data["player_chops"].remove(self.groups_data["player_chops"])
        self.chop_ready = True

    # Возрождение
    def revival(self):
        self.health_points = constants.PLAYER_MAX_HEALTH_POINTS
        self.rect.x = self.respawn_coord[0]
        self.rect.y = self.respawn_coord[1]
        self.pointer.side_update(self.pointer.side)
        self.groups_data["player_chops"].remove(self.groups_data["player_chops"])
