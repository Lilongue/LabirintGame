"""
Цвета и константы для игры-лабиринта
"""

from enum import Enum

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

# Константы игры
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Размеры областей
MAZE_WIDTH = 800
MAZE_HEIGHT = 600
MAZE_START_X = 20
MAZE_START_Y = 20

CODE_PANEL_WIDTH = 360
CODE_PANEL_X = MAZE_START_X + MAZE_WIDTH + 20

# Размеры лабиринта по умолчанию
DEFAULT_MAZE_WIDTH = 19
DEFAULT_MAZE_HEIGHT = 15

EASY_MAZE_WIDTH = 13
EASY_MAZE_HEIGHT = 9
