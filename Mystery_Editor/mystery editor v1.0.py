import sys

import pygame

from main import Scene
import game_stuff
from game_stuff import *
from player import Player
from level_updater import *


pygame.init()


class LevelEditorScene(Scene):
    def __init__(self, **kwargs):
        super(LevelEditorScene, self).__init__(**kwargs)
        self.available_objects = game_stuff.available_objects
        self.fps_show = False
        self.active_object = self.available_objects[0]
        self.level_date = get_level("created_level.lvl")
        self.mouse_pressing_add_obj = False
        self.mouse_pressing_remove_obj = False

    def play(self, m_visible=False):
        pygame.mouse.set_visible(m_visible)
        load_level("created_level.lvl", self.groups_data)
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
                if event.key == pygame.K_c:  # Очистка уровня
                    for key in self.groups_data:
                        self.groups_data[key].remove(self.groups_data[key])
                    self.level_date = [["."] * 22 for _ in range(12)]
                    self.update_level()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_pressing_add_obj = True
                elif event.button == 3:
                    self.mouse_pressing_remove_obj = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressing_remove_obj = False
                self.mouse_pressing_add_obj = False

            if self.mouse_pressing_add_obj:
                self.add_object(event.pos)
            if self.mouse_pressing_remove_obj:
                self.remove_object(event.pos)
        for key in self.groups_data:
            self.groups_data[key].update()

    def add_object(self, coordination):
        self.level_date[coordination[1] // 64][coordination[0] // 64] = self.active_object
        self.update_level()

    def remove_object(self, coordination):
        for key in self.groups_data:
            self.groups_data[key].remove(self.groups_data[key])
        self.level_date[coordination[1] // 64][coordination[0] // 64] = "."
        self.update_level()

    def update_level(self):
        for key in self.groups_data:
            self.groups_data[key].remove(self.groups_data[key])
        change_level("created_level.lvl", self.level_date)
        load_level("created_level.lvl", self.groups_data)


if __name__ == '__main__':
    scene = LevelEditorScene()
    scene.play(m_visible=True)
