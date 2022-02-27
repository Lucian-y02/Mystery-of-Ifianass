import threading
import time

import pygame

from game_stuff import *


pygame.init()


# Противник
class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups: dict, coord, target, size=(38, 42), max_health_points=100):
        super(Enemy, self).__init__(groups["enemies"])
        self.image = pygame.Surface(size)
        self.image.fill((200, 204, 194))
        self.rect = self.image.get_rect()
        self.rect.x = coord[0] + 13
        self.rect.y = coord[1] + 11

        self.groups_data = groups

        # Характеристики
        self.max_health_points = max_health_points  # Максимальео количество здоровья
        self.health_points = self.max_health_points
        self.target_list = [target]  # Список возможных целей
        self.target = target  # Цель
        HealthPointsIndicator(groups["game_stuff"], self, size=(self.rect.width, 4))

    def update(self):
        if self.health_points <= 0:
            self.kill()
        self.check_collision()

    def check_collision(self):
        for chop in self.groups_data["player_chops"]:
            if self.rect.colliderect(chop.rect) and chop.tangible:
                self.health_points -= chop.damage
                chop.tangible = False
