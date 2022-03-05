import pygame

from player import Player
from game_stuff import *


pygame.init()


# Получение матрицы уровня
def get_level(path):
    with open(path, "r") as level:
        return list(map(lambda lvl: list(lvl.rstrip("\n")), level.readlines()))


def change_level(path, level_data):
    with open(path, "w") as level:
        level.write("\n".join(["".join(x) for x in level_data]))
        level.close()


# Загрузка уровня
def load_level(path, groups_data):
    player_be = False  # Наличие игрока
    level_data = get_level(path)
    for x in range(22):
        for y in range(12):
            label = level_data[y][x]
            # Игрок
            if label == "@" and not player_be:
                Player(groups_data, (x * 64, y * 64), control_function="game_pad")
            elif label == "b":
                Box(groups_data["game_stuff"], (x * 64, y * 64))
            elif label == "-":
                HorizontalWall(groups_data["game_stuff"], (x * 64, y * 64))
            elif label == "_":
                HorizontalWall(groups_data["game_stuff"], (x * 64, y * 64 + 64))
            elif label == "[":
                VerticalWall(groups_data["game_stuff"], (x * 64, y * 64))
            elif label == "]":
                VerticalWall(groups_data["game_stuff"], (x * 64 + 64, y * 64))
            elif label == "1":
                HorizontalWall(groups_data["game_stuff"], (x * 64, y * 64))
                VerticalWall(groups_data["game_stuff"], (x * 64, y * 64))
            elif label == "2":
                HorizontalWall(groups_data["game_stuff"], (x * 64, y * 64))
                VerticalWall(groups_data["game_stuff"], (x * 64 + 64, y * 64))
            elif label == "3":
                HorizontalWall(groups_data["game_stuff"], (x * 64, y * 64 + 64))
                VerticalWall(groups_data["game_stuff"], (x * 64, y * 64))
            elif label == "4":
                HorizontalWall(groups_data["game_stuff"], (x * 64, y * 64 + 64))
                VerticalWall(groups_data["game_stuff"], (x * 64 + 64, y * 64))
