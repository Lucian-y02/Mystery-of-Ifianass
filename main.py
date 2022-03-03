import sys

import pygame

from level_editor import load_level
from enemies import *


class Scene:
    def __init__(self, **kwargs):
        self.screen = pygame.display.set_mode(kwargs.get("size", (1280, 1024)), pygame.FULLSCREEN)
        self.background_color = kwargs.get("background_color", (27, 29, 31))  # Цвет фона
        self.background_image = pygame.image.load("level0.png").convert_alpha()
        # Группы спрайтов
        self.groups_data = {
            "player": pygame.sprite.Group(),  # Игрок
            "player_chops": pygame.sprite.Group(),  # Удары игрока
            "enemies": pygame.sprite.Group(),  # Проитвники
            "game_stuff": pygame.sprite.Group()  # Различные игровые объекты
        }
        self.clock = pygame.time.Clock()
        self.FPS = kwargs.get("FPS", 60)
        self.game_run = True

        self.draw_grid = False  # Рисование сетки
        self.fps_show = True  # Отображение FPS

        self.default_font = pygame.font.Font(None, 24)  # Стандартный шрифт

    def play(self):
        load_level("Levels/level_0.lvl", self.groups_data)
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
                if event.key == pygame.K_f:
                    self.fps_show = not self.fps_show
        for key in self.groups_data:
            self.groups_data[key].update()

    def draw(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.background_image, (0, 0))
        for key in self.groups_data:
            self.groups_data[key].draw(self.screen)
        if self.draw_grid:
            for x in range(self.screen.get_width() // 64 + 1):
                pygame.draw.line(self.screen, (200, 204, 194),
                                 (64 * x, 0), (64 * x, self.screen.get_height()))
            for y in range(self.screen.get_height() // 64):
                pygame.draw.line(self.screen, (200, 204, 194),
                                 (0, 64 * y), (self.screen.get_width(), 64 * y))
        if self.fps_show:
            self.screen.blit(self.default_font.render(f"FPS {str(round(self.clock.get_fps()))}",
                                                      False, (200, 204, 194)), (20, 20))


if __name__ == '__main__':
    pygame.init()
    scene = Scene()

    scene.play()
