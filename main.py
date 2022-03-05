import sys

from Mystery_Editor import level_updater
from enemies import *


class Scene:
    def __init__(self, **kwargs):
        self.screen = pygame.display.set_mode(kwargs.get("size", (1280, 1024)), pygame.FULLSCREEN)
        self.background_color = kwargs.get("background_color", (27, 29, 31))  # Цвет фона
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

    def play(self, m_visible=False):
        pygame.mouse.set_visible(m_visible)
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

    def load_level(self, path):
        for key in self.groups_data:
            if key != "player":
                self.groups_data[key].remove()
        level_updater.load_level(path, self.groups_data)


if __name__ == '__main__':
    pygame.init()
    scene = Scene()
    scene.load_level("Levels/level_0.lvl")

    scene.play()
