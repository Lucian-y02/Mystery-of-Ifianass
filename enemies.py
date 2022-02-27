import threading
import time

import pygame

from game_stuff import *


pygame.init()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups: dict, coordinates, size=(38, 42), max_health_points=100):
        super(Enemy, self).__init__(groups["enemies"])
        self.image = pygame.Surface(size)
        self.image.fill((200, 204, 194))
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0] + 13
        self.rect.y = coordinates[1] + 11

        self.groups_data = groups

        self.max_health_points = max_health_points
        self.health_points = self.max_health_points
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
