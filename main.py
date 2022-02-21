import sys

import pygame

from player import Player
from game_stuff import *


class Scene:
    def __init__(self, **kwargs):
        self.screen = pygame.display.set_mode(kwargs.get("size", (1280, 1024)), pygame.FULLSCREEN)
        self.background_color = kwargs.get("background_color", (27, 29, 31))  # Цвет фона
        # Группы спрайтов
        self.groups_data = {
            "player": pygame.sprite.Group(),
            "enemy": pygame.sprite.Group(),
            "game_stuff": pygame.sprite.Group()
        }
        self.clock = pygame.time.Clock()
        self.FPS = kwargs.get("FPS", 60)
        self.game_run = True

        self.draw_grid = False  # Рисование сетки

    def play(self):
        pygame.mouse.set_visible(False)
        while self.game_run:
            self.check_events()
            self.draw()

            self.clock.tick(self.FPS)
            pygame.display.update()
        sys.exit(pygame.quit())

    def check_events(self):
        for event in pygame.event.get():
            if ((event.type == pygame.KEYUP and event.key == pygame.K_DELETE) or
                    event.type == pygame.QUIT):
                self.game_run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    self.draw_grid = not self.draw_grid
        for key in self.groups_data:
            self.groups_data[key].update()

    def draw(self):
        self.screen.fill(self.background_color)
        for key in self.groups_data:
            self.groups_data[key].draw(self.screen)
        if self.draw_grid:
            for x in range(self.screen.get_width() // 64 + 1):
                pygame.draw.line(self.screen, (200, 204, 194),
                                 (64 * x, 0), (64 * x, self.screen.get_height()))
            for y in range(self.screen.get_height() // 64):
                pygame.draw.line(self.screen, (200, 204, 194),
                                 (0, 64 * y), (self.screen.get_width(), 64 * y))


if __name__ == '__main__':
    pygame.init()
    scene = Scene()

    player = Player(scene.groups_data, x=64 * 5, y=64 * 4,
                    control_function="game_pad")
    Box(scene.groups_data["game_stuff"], 64 * 7, 64 * 6)

    scene.play()
