import sys

from Mystery_Editor import level_updater
from enemies import *


class Scene:
    def __init__(self, **kwargs):
        self.screen = pygame.display.set_mode(kwargs.get("size", (1920, 1080)), pygame.FULLSCREEN)
        self.background_color = kwargs.get("background_color", (27, 29, 31))  # Цвет фона
        # Группы спрайтов
        self.groups_data = {
            "walls": pygame.sprite.Group(),  # Стены (должны быть невидимыми)
            "kill_zones": pygame.sprite.Group(),  # Зоны поражения
            "enemies": pygame.sprite.Group(),  # Проитвники
            "game_stuff": pygame.sprite.Group(),  # Различные игровые объекты
            "player": pygame.sprite.Group(),  # Игрок
            "player_chops": pygame.sprite.Group(),  # Удары игрока
            "doors": pygame.sprite.Group(),  # Двери
            "text": pygame.sprite.Group()  # Текст
        }
        self.clock = pygame.time.Clock()
        self.FPS = kwargs.get("FPS", 60)
        self.game_run = True

        self.draw_grid = False  # Рисование сетки
        self.fps_show = True  # Отображение FPS

        self.default_font = pygame.font.Font(None, 24)  # Стандартный шрифт

        self.level_path_now = str()

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
                if event.key == pygame.K_r:
                    self.load_level_on_scene(self.level_path_now)
        for key in self.groups_data:
            self.groups_data[key].update()

    def draw(self):
        self.screen.fill(self.background_color)
        if self.draw_grid:
            for x in range(self.screen.get_width() // 64 + 1):
                pygame.draw.line(self.screen, (50, 54, 44),
                                 (64 * x, 0), (64 * x, self.screen.get_height()))
            for y in range(self.screen.get_height() // 64):
                pygame.draw.line(self.screen, (50, 54, 44),
                                 (0, 64 * y), (self.screen.get_width(), 64 * y))
        for key in self.groups_data:
            self.groups_data[key].draw(self.screen)
        if self.fps_show:
            self.screen.blit(self.default_font.render(f"FPS {str(round(self.clock.get_fps()))}",
                                                      False, (200, 204, 194)), (20, 20))

    # Очистка уровня
    def clear_groups_data(self):
        for key in self.groups_data:
            self.groups_data[key].remove(self.groups_data[key])

    # Загрузка уровня
    def load_level_on_scene(self, path):
        self.level_path_now = path
        self.clear_groups_data()
        level_updater.load_level(path, self.groups_data)


if __name__ == '__main__':
    pygame.init()
    scene = Scene()
    # scene.load_level_on_scene("Levels/Demo levels/demo_level_1.json")
    # scene.load_level_on_scene("Levels/Demo levels/demo_level_2.json")
    # scene.load_level_on_scene("Levels/Demo levels/demo_level_3.json")
    scene.load_level_on_scene("Levels/Demo levels/demo_level_5.json")
    # scene.load_level_on_scene("Levels/level_0.json")

    scene.play()
