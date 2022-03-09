import sys

import pygame

from main import Scene
import game_stuff
from game_stuff import *
from player import Player
from level_updater import *


pygame.init()

available_objects = get_available_objects()


class LevelEditorScene(Scene):
    def __init__(self, **kwargs):
        super(LevelEditorScene, self).__init__(**kwargs)
        self.available_objects = available_objects
        self.fps_show = False
        self.draw_grid = True
        self.active_object = "Box"  # Размещаемый объект
        self.level_date = get_level("created_level.json")
        self.mouse_pressing_add_obj = False  # Удерживается левая клавиша мыши (добавление)
        self.mouse_pressing_remove_obj = False  # Удераживается правая клавиша мыши (удаление)
        self.take_object_mod = False  # Режим выбора размещаемого объекта

    def play(self, m_visible=False):
        pygame.mouse.set_visible(m_visible)
        self.load_level_on_scene("created_level.json")
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
                if event.key == pygame.K_f:
                    self.fps_show = not self.fps_show
                elif event.key == pygame.K_c and not self.take_object_mod:  # Очистка уровня
                    for key in self.groups_data:
                        self.groups_data[key].remove(self.groups_data[key])
                    self.level_date = dict()
                    self.update_level("created_level.json")
                elif event.key == pygame.K_TAB:  # Выбор объекта
                    self.take_object_mod = not self.take_object_mod
                    self.draw_grid = not self.draw_grid
                    if self.take_object_mod:
                        self.load_level_on_scene("take_object_mod_list.json")
                    else:
                        self.load_level_on_scene("created_level.json")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.take_object_mod:
                    if event.button == 1:
                        self.mouse_pressing_add_obj = True
                    elif event.button == 3:
                        self.mouse_pressing_remove_obj = True
                else:  # Выбор объекта
                    coord = f"{event.pos[0] // 64} {event.pos[1] // 64}"
                    new_active_object = get_level("take_object_mod_list.json").get(coord,
                                                                                   [None])[0]
                    if new_active_object:
                        self.active_object = new_active_object
                        self.take_object_mod = False
                        self.draw_grid = True
                        self.load_level_on_scene("created_level.json")
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressing_remove_obj = False
                self.mouse_pressing_add_obj = False

            if self.mouse_pressing_add_obj:
                self.add_object(event.pos)
            if self.mouse_pressing_remove_obj:
                self.remove_object(event.pos)
        # Попробовать сделать без этого !!!
        # for key in self.groups_data:
        #     self.groups_data[key].update()

    def add_object(self, coord):
        self.level_date[f"{coord[0] // 64} {coord[1] // 64}"] = [self.active_object, {}]
        self.update_level("created_level.json")

    def remove_object(self, coord):
        self.clear_groups_data()
        self.level_date.pop(f"{coord[0] // 64} {coord[1] // 64}", None)
        self.update_level("created_level.json")

    def update_level(self, path):
        self.clear_groups_data()
        change_level(path, self.level_date)
        load_level(path, self.groups_data)


if __name__ == '__main__':
    scene = LevelEditorScene()
    scene.play(m_visible=True)
