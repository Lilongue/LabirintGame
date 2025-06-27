# Interface Description File
from enum import Enum

# file: colors.py
class Colors:
    """Цветовая схема игры"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    BLUE = (0, 100, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (64, 64, 64)
    BROWN = (139, 69, 19)
    ORANGE = (255, 165, 0)

class GameState(Enum):
    """Состояния игры"""
    MENU = 1
    PLAYING = 2
    EDITING_CODE = 3
    EXECUTING = 4
    GAME_OVER = 5

class CellType(Enum):
    """Типы клеток лабиринта"""
    WALL = 0
    PATH = 1
    START = 2
    FINISH = 3

#file: maze.py
class Maze:
    """Класс для генерации и управления лабиринтом"""
    def __init__(self, width=13, height=9):
        ...
    def generate_maze(self):
        """Генерация лабиринта алгоритмом рекурсивного backtracking"""
        ...
    def ensure_finish_accessible(self):
        ...
    def get_cell_type(self, x, y):
        ...
    def is_valid_move(self, x, y):
        ...
    def is_finish(self, x, y):
        ...
    def get_maze_info(self):
        ...

    #file: player.py
    class Player:
        ...
        def __init__(self, start_x, start_y):
            ...
        def reset_position(self):
            ...
        def set_start_position(self, x, y):
            ...
        def move_to(self, new_x, new_y):
            ...
        def get_position(self):
            ...
        def get_stats(self):
            ...
        def is_at_finish(self, finish_pos: tuple):
            ...

    class CommandInterpreter:
        """Интерпретатор команд для управления игроком"""
        def __init__(self, player, maze):
            ...
        def clear_logs(self):
            ...
        def log_move(self, command, success, message=""):
            ...
        def move_up(self):
            ...
        def move_down(self):
            ...
        def move_left(self):
            ...
        def move_right(self):
            ...
        def get_position(self):
            ...
        def is_at_finish(self):
            ...
        def execute_code(self, code):
            ...
        def get_execution_summary(self):
            ...

#file: ui.py
class UI:
    ...
    def __init__(self, screen):
        ...

    def draw_maze(self, maze, player):
        ...
    def draw_code_panel(self, editing_code=False):
        ...
    def draw_buttons(self):
        ...
    def draw_hints(self):
        ...
    def draw_menu(self):
        ...
    
    def get_button_rects(self):
        """Получить прямоугольники кнопок для обработки кликов"""
        ...
    def set_code_text(self, text):
        ...
    def get_code_text(self):
        ...
    def set_output_text(self, text):
        ... 
    def add_character(self, char):
        ...
    def remove_character(self):
        ...

#file: main.py
class MazeGame:
    def __init__(self):
        ...

    def run(self):
        """Основной цикл игры"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        """Обработка событий"""
        ...

    def handle_menu_events(self, event):
        """Обработка событий в меню"""
        ...

    def handle_playing_events(self, event):
        """Обработка событий во время игры"""
        ...

    def handle_editing_code_events(self, event):
        """Обработка событий при редактировании кода"""
        ...

    def handle_executing_events(self, event):
        """Обработка событий при выполнении кода"""
        ...

    def update(self):
        """Обновление состояния игры"""
        ...

    def draw(self):
        """Отрисовка элементов игры"""
        ...

    def execute_code(self):
        """Выполнение пользовательского кода"""
        ...

    def reset_game(self):
        """Сброс игры"""
        ...

    def draw_game_over_screen(self):
        """Экран завершения игры"""
        ...
