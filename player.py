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
        self.image = pygame.Surface((kwargs.get("size", (44, 64))))
        self.image.fill(kwargs.get("color", (200, 204, 194)))
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + 12
        self.rect.y = coord[1]

        # Геймпад
        self.game_pad = None
        try:
            self.game_pad = pygame.joystick.Joystick(0)
        except pygame.error:
            pass

        # Характеристики
        self.default_speed = constants.player_speed
        self.speed = self.default_speed

        # Перемещение
        self.move_x = 0
        self.move_y = 0

        # Управление
        self.control_data = {
            "keyboard": self.keyboard_check_pressing,
            "game_pad": self.game_pad_check_pressing
        }
        self.control_function = self.control_data[kwargs.get("control_function", "keyboard")]

        self.pointer = Pointer(self.groups_data["game_stuff"], self)  # Указатель

        # Атака
        self.chop_cool_down = kwargs.get("shop_cool_down", 1)
        self.chop_ready = True  # Возможность провести атаку
        self.do_chop = True  # Атака

        # Рывок
        self.dash_cool_down = kwargs.get("dash_cool_down", 1)
        self.dash_ready = True  # Возможность сделать рывок
        self.do_dash = False  # Рывок
        self.dash_duration = kwargs.get("dash_duration", 0.35)  # Время продолжительности рывка

    def update(self):
        self.move_x = 0
        self.move_y = 0

        # Ослеживание нажатий
        self.control_function()

        # Рывок
        if self.do_dash:
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

        # Отслеживание столкновений
        self.check_collision()

    # Управление клавиатурой
    def keyboard_check_pressing(self):
        key = pygame.key.get_pressed()

        # Вверх
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.move_y -= self.speed
            self.pointer.side_update("UP")
        # Вниз
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.move_y += self.speed
            self.pointer.side_update("DOWN")
        # Вправо
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.move_x += self.speed
            self.pointer.side_update("RIGHT")
        # Влево
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.move_x -= self.speed
            self.pointer.side_update("LEFT")
        # Удар
        if key[pygame.K_j] and self.chop_ready:
            Chop(self.groups_data["player_chops"], self, damage=60)
            self.speed = 0
            self.chop_ready = False
            threading.Thread(target=self.chop_timer_reloading).start()
        # Рывок
        if key[pygame.K_k] and self.dash_ready and not self.do_dash:
            self.dash_ready = False
            self.do_dash = True
            self.speed = 0
            self.do_chop = False
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
        if self.game_pad.get_button(2) and self.chop_ready and self.do_chop:
            Chop(self.groups_data["player_chops"], self, damage=60)
            self.speed = 0
            self.chop_ready = False
            threading.Thread(target=self.chop_timer_reloading).start()
        # Рывок
        if self.game_pad.get_button(0) and self.dash_ready and not self.do_dash:
            self.dash_ready = False
            self.do_dash = True
            self.speed = 0
            self.do_chop = False
            threading.Thread(target=self.dash_timer).start()

    # Столкновения
    def check_collision(self):
        for obj in self.groups_data["game_stuff"]:
            if (self.rect.colliderect(obj.rect) and
                    obj.__class__.__name__ == "VerticalWall"):
                if (abs(self.rect.x + self.rect.width - obj.rect.x) >
                        abs(self.rect.x - obj.rect.x)):
                    self.rect.x += self.default_speed
                else:
                    self.rect.x -= self.default_speed
                self.move_x = 0
            if (self.rect.colliderect(obj.rect) and
                    obj.__class__.__name__ == "HorizontalWall"):
                if (abs(self.rect.y - obj.rect.y) >
                        abs(self.rect.y + self.rect.width - obj.rect.y)):
                    self.rect.y -= self.default_speed
                else:
                    self.rect.y += self.default_speed
                self.move_y = 0

    # Таймер, по истечению которого можно провести следующую атаку
    def chop_timer_reloading(self):
        time.sleep(self.chop_cool_down)
        self.chop_ready = True

    # Таймер, по истечению которого можно использовать рываок
    def dash_timer_reloading(self):
        time.sleep(self.dash_cool_down)
        self.dash_ready = True

    # Таймер, по истечению которого рывок заканчивается
    def dash_timer(self):
        time.sleep(self.dash_duration)
        self.do_dash = False
        self.speed = self.default_speed
        self.do_chop = True
        self.pointer.side_update(self.pointer.side)
        threading.Thread(target=self.dash_timer_reloading).start()
