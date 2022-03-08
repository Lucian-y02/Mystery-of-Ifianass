import threading
import time

import pygame

from game_stuff import *


pygame.init()


# Противник
class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups: dict, coord, **kwargs):
        super(Enemy, self).__init__(groups["enemies"])
        self.image = pygame.Surface(kwargs.get("size", (38, 42)))
        self.image.fill((200, 204, 194))
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + 13
        self.rect.y = coord[1] + 11

        self.groups_data = groups

        # Характеристики
        # Максимальео количество здоровья
        self.max_health_points = kwargs.get("max_health_points", 100)
        self.health_points = self.max_health_points
        self.target_list = [kwargs.get("target", None)]  # Список возможных целей
        self.target = self.target_list[0]  # Цель
        HealthPointsIndicator(groups["game_stuff"], self, size=(self.rect.width, 4))
        print("ok")

    def update(self):
        if self.health_points <= 0:
            self.kill()
        self.check_collision()

    def check_collision(self):
        for chop in self.groups_data["player_chops"]:
            if self.rect.colliderect(chop.rect) and chop.tangible:
                self.health_points -= chop.damage
                chop.tangible = False
