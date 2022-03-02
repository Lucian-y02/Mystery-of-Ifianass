import pygame

from player import Player
from game_stuff import *


pygame.init()


# Загрузка уровня
def load_level(path, groups_data):
    player_be = False  # Наличие игрока
    with open(path, "r") as level:
        level_data = list(map(lambda lvl: lvl.rstrip("\n"), level.readlines()))
        for x in range(21):
            for y in range(12):
                label = level_data[y][x]
                # Игрок
                if label == "@" and not player_be:
                    Player(groups_data, (x * 64, y * 64), control_function="game_pad")
                if label == "b":
                    Box(groups_data["game_stuff"], (x * 64, y * 64))
