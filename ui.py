"""
Модуль пользовательского интерфейса
"""

import pygame
from colors import Colors, CellType, WINDOW_WIDTH, WINDOW_HEIGHT
from colors import MAZE_START_X, MAZE_START_Y, MAZE_WIDTH, MAZE_HEIGHT
from colors import CODE_PANEL_X, CODE_PANEL_WIDTH

class UI:
    """Класс для отрисовки пользовательского интерфейса"""
    
    def __init__(self, screen):
        self.screen = screen
        
        # Шрифты
        self.font_small = pygame.font.Font(None, 18)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
        
        # Состояние UI
        self.code_text = ""
        self.output_text = "Добро пожаловать в игру!\nВведите команды для движения игрока."
    
    def draw_maze(self, maze, player):
        """Отрисовка лабиринта и игрока"""
        # Вычисление размера клетки
        cell_size = min(MAZE_WIDTH // maze.width, MAZE_HEIGHT // maze.height)
        
        # Фон лабиринта
        maze_rect = pygame.Rect(MAZE_START_X, MAZE_START_Y, MAZE_WIDTH, MAZE_HEIGHT)
        pygame.draw.rect(self.screen, Colors.WHITE, maze_rect)
        pygame.draw.rect(self.screen, Colors.BLACK, maze_rect, 2)
        
        # Отрисовка клеток лабиринта
        for y in range(maze.height):
            for x in range(maze.width):
                cell_type = maze.get_cell_type(x, y)
                
                # Вычисление позиции клетки на экране
                screen_x = MAZE_START_X + x * cell_size
                screen_y = MAZE_START_Y + y * cell_size
                
                cell_rect = pygame.Rect(screen_x, screen_y, cell_size, cell_size)
                
                # Выбор цвета в зависимости от типа клетки
                if cell_type == CellType.WALL:
                    pygame.draw.rect(self.screen, Colors.BROWN, cell_rect)
                elif cell_type == CellType.PATH:
                    pygame.draw.rect(self.screen, Colors.WHITE, cell_rect)
                elif cell_type == CellType.START:
                    pygame.draw.rect(self.screen, Colors.GREEN, cell_rect)
                elif cell_type == CellType.FINISH:
                    pygame.draw.rect(self.screen, Colors.ORANGE, cell_rect)
                
                # Границы клеток для лучшей видимости
                pygame.draw.rect(self.screen, Colors.LIGHT_GRAY, cell_rect, 1)
        
        # Отрисовка игрока
        player_screen_x = MAZE_START_X + player.x * cell_size
        player_screen_y = MAZE_START_Y + player.y * cell_size
        
        # Игрок как красный круг с небольшим отступом
        center_x = player_screen_x + cell_size // 2
        center_y = player_screen_y + cell_size // 2
        radius = cell_size // 3
        
        pygame.draw.circle(self.screen, Colors.RED, (center_x, center_y), radius)
        pygame.draw.circle(self.screen, Colors.BLACK, (center_x, center_y), radius, 2)
        
        # Информация о лабиринте
        info_y = MAZE_START_Y + MAZE_HEIGHT + 10
        stats = player.get_stats()
        info_text = f"Игрок: {stats['position']} | Ходов: {stats['moves']} | "
        info_text += f"Финиш: {maze.finish_pos} | Размер: {maze.width}x{maze.height}"
        
        info_surface = self.font_small.render(info_text, True, Colors.BLACK)
        self.screen.blit(info_surface, (MAZE_START_X, info_y))
    
    def draw_code_panel(self, editing_code=False):
        """Отрисовка панели с кодом"""
        # Фон панели
        panel_rect = pygame.Rect(CODE_PANEL_X, 20, CODE_PANEL_WIDTH, WINDOW_HEIGHT - 40)
        pygame.draw.rect(self.screen, Colors.WHITE, panel_rect)
        pygame.draw.rect(self.screen, Colors.BLACK, panel_rect, 2)
        
        # Заголовок
        title_text = self.font_large.render("Панель кода", True, Colors.BLACK)
        self.screen.blit(title_text, (CODE_PANEL_X + 10, 30))
        
        # Область ввода кода
        code_rect = pygame.Rect(CODE_PANEL_X + 10, 70, CODE_PANEL_WIDTH - 20, 200)
        color = Colors.YELLOW if editing_code else Colors.LIGHT_GRAY
        pygame.draw.rect(self.screen, color, code_rect)
        pygame.draw.rect(self.screen, Colors.BLACK, code_rect, 1)
        
        # Текст кода
        if self.code_text:
            lines = self.code_text.split('\n')
            for i, line in enumerate(lines[-8:]):  # Показываем последние 8 строк
                text_surface = self.font_small.render(line, True, Colors.BLACK)
                self.screen.blit(text_surface, (CODE_PANEL_X + 15, 75 + i * 20))
        
        # Курсор при редактировании
        if editing_code:
            cursor_x = CODE_PANEL_X + 15 + len(self.code_text.split('\n')[-1]) * 8
            cursor_y = 75 + (len(self.code_text.split('\n')) - 1) * 20
            pygame.draw.line(self.screen, Colors.BLACK, 
                           (cursor_x, cursor_y), (cursor_x, cursor_y + 18), 2)
        
        # Область вывода
        output_rect = pygame.Rect(CODE_PANEL_X + 10, 290, CODE_PANEL_WIDTH - 20, 200)
        pygame.draw.rect(self.screen, Colors.LIGHT_GRAY, output_rect)
        pygame.draw.rect(self.screen, Colors.BLACK, output_rect, 1)
        
        # Текст вывода
        output_label = self.font_medium.render("Вывод:", True, Colors.BLACK)
        self.screen.blit(output_label, (CODE_PANEL_X + 15, 295))
        
        lines = self.output_text.split('\n')
        for i, line in enumerate(lines[:8]):  # Показываем первые 8 строк
            text_surface = self.font_small.render(line, True, Colors.DARK_GRAY)
            self.screen.blit(text_surface, (CODE_PANEL_X + 15, 320 + i * 20))
    
    def draw_buttons(self):
        """Отрисовка кнопок управления"""
        button_y = WINDOW_HEIGHT - 60
        
        # Кнопка "Выполнить"
        execute_btn = pygame.Rect(CODE_PANEL_X + 10, button_y, 100, 40)
        pygame.draw.rect(self.screen, Colors.GREEN, execute_btn)
        pygame.draw.rect(self.screen, Colors.BLACK, execute_btn, 2)
        execute_text = self.font_medium.render("Выполнить", True, Colors.BLACK)
        text_rect = execute_text.get_rect(center=execute_btn.center)
        self.screen.blit(execute_text, text_rect)
        
        # Кнопка "Очистить"
        clear_btn = pygame.Rect(CODE_PANEL_X + 120, button_y, 100, 40)
        pygame.draw.rect(self.screen, Colors.YELLOW, clear_btn)
        pygame.draw.rect(self.screen, Colors.BLACK, clear_btn, 2)
        clear_text = self.font_medium.render("Очистить", True, Colors.BLACK)
        text_rect = clear_text.get_rect(center=clear_btn.center)
        self.screen.blit(clear_text, text_rect)
        
        # Кнопка "Новый лабиринт"
        new_maze_btn = pygame.Rect(CODE_PANEL_X + 230, button_y, 120, 40)
        pygame.draw.rect(self.screen, Colors.BLUE, new_maze_btn)
        pygame.draw.rect(self.screen, Colors.BLACK, new_maze_btn, 2)
        new_text = self.font_small.render("Новый лабиринт", True, Colors.WHITE)
        text_rect = new_text.get_rect(center=new_maze_btn.center)
        self.screen.blit(new_text, text_rect)
    
    def draw_hints(self):
        """Отрисовка подсказок"""
        hint_y = 520
        hints = [
            "F1 - Меню",
            "F2 - Игра", 
            "ESC - Выход",
            "Кликните в поле кода для ввода"
        ]
        
        for i, hint in enumerate(hints):
            hint_text = self.font_small.render(hint, True, Colors.DARK_GRAY)
            self.screen.blit(hint_text, (CODE_PANEL_X + 15, hint_y + i * 20))
    
    def draw_menu(self):
        """Отрисовка главного меню"""
        # Фон
        self.screen.fill(Colors.DARK_GRAY)
        
        # Заголовок
        title = self.font_large.render("ЛАБИРИНТ С ПРОГРАММИРОВАНИЕМ", True, Colors.WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        # Описание
        description = [
            "Управляйте персонажем с помощью команд Python!",
            "",
            "Доступные команды:",
            "• move_up() - движение вверх",
            "• move_down() - движение вниз", 
            "• move_left() - движение влево",
            "• move_right() - движение вправо",
            "",
            "Нажмите F2 для начала игры"
        ]
        
        for i, line in enumerate(description):
            text = self.font_medium.render(line, True, Colors.WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 300 + i * 30))
            self.screen.blit(text, text_rect)
    
    def get_button_rects(self):
        """Получить прямоугольники кнопок для обработки кликов"""
        button_y = WINDOW_HEIGHT - 60
        return {
            'execute': pygame.Rect(CODE_PANEL_X + 10, button_y, 100, 40),
            'clear': pygame.Rect(CODE_PANEL_X + 120, button_y, 100, 40),
            'new_maze': pygame.Rect(CODE_PANEL_X + 230, button_y, 120, 40),
            'code_area': pygame.Rect(CODE_PANEL_X + 10, 70, CODE_PANEL_WIDTH - 20, 200)
        }
    
    def set_code_text(self, text):
        """Установить текст кода"""
        self.code_text = text
    
    def get_code_text(self):
        """Получить текст кода"""
        return self.code_text
    
    def set_output_text(self, text):
        """Установить текст вывода"""
        self.output_text = text
    
    def add_character(self, char):
        """Добавить символ к коду"""
        self.code_text += char
    
    def remove_character(self):
        """Удалить последний символ из кода"""
        if self.code_text:
            self.code_text = self.code_text[:-1]