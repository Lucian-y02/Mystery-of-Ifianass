import json
import pygame

from player import Player
from game_stuff import *
from enemies import Enemy


pygame.init()

# Доступные для размещения на уровне объекты
available_objects = {
    "Player": [Player, "all_the_groups"],
    "Box": [Box, "walls"],
    "NorthWall": [NorthWall, "walls"],
    "SouthWall": [SouthWall, "walls"],
    "WesternWall": [WesternWall, "walls"],
    "EastWall": [EastWall, "walls"],
    "TopLeftCorner": [TopLeftCorner, "walls"],
    "TopRightCorner": [TopRightCorner, "walls"],
    "DownLeftCorner": [DownLeftCorner, "walls"],
    "DownRightCorner": [DownRightCorner, "walls"],
    "MiddleHorizontalPlatform": [MiddleHorizontalPlatform, "walls"],
    "WesternHorizontalPlatform": [WesternHorizontalPlatform, "walls"],
    "EastHorizontalPlatform": [EastHorizontalPlatform, "walls"],
    "MiddleVerticalPlatform": [MiddleVerticalPlatform, "walls"],
    "NorthVerticalPlatform": [NorthVerticalPlatform, "walls"],
    "SouthVerticalPlatform": [SouthVerticalPlatform, "walls"],
    "MobileObject": [MobileObject, "all_the_groups"],
    "KillZone": [KillZone, "kill_zones"],
    "WesternKillZone": [WesternKillZone, "kill_zones"],
    "EastKillZone": [EastKillZone, "kill_zones"],
    "NorthKillZone": [NorthKillZone, "kill_zones"],
    "SouthKillZone": [SouthKillZone, "kill_zones"],
    "TopLeftKillZoneCorner": [TopLeftKillZoneCorner, "kill_zones"],
    "DownLeftKillZoneCorner": [DownLeftKillZoneCorner, "kill_zones"],
    "TopRightKillZoneCorner": [TopRightKillZoneCorner, "kill_zones"],
    "DownRightKillZoneCorner": [DownRightKillZoneCorner, "kill_zones"],
    "VerticalSingleKillZone":[VerticalSingleKillZone, "kill_zones"],
    "HorizontalSingleKillZone": [HorizontalSingleKillZone, "kill_zones"],
    "SingleKillZoneCorner": [SingleKillZoneCorner, "kill_zones"]
}


def get_available_objects():
    return available_objects


# Получение матрицы уровня
def get_level(path):
    with open(path, "r") as level:
        return json.load(level)


# Запись изменения уровня
def change_level(path, level_data):
    with open(path, "w") as level:
        json.dump(level_data, level)
        level.close()


# Загрузка уровня
def load_level(path, groups_data):
    level_data = get_level(path)
    for key in level_data:
        # Объект
        obj = available_objects[level_data[key][0]][0]
        # Группа или группы
        obj_group = groups_data \
            if available_objects[level_data[key][0]][1] == "all_the_groups" else \
            groups_data[available_objects[level_data[key][0]][1]]
        # Координаты
        obj_coord = (int(key.split()[0]) * 64, int(key.split()[1]) * 64)
        # Именованные аргументы
        obj_kwargs = level_data[key][1]
        # Создание объекта
        obj(obj_group, obj_coord, **obj_kwargs)
