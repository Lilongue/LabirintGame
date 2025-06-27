"""
Модуль для генерации и управления лабиринтом
"""

import random
from colors import CellType

class Maze:
    """Класс для генерации и управления лабиринтом"""
    
    def __init__(self, width=13, height=9):
        self.width = width  # Должно быть нечетным для правильной генерации
        self.height = height  # Должно быть нечетным для правильной генерации
        self.grid = []
        self.start_pos = (1, 1)
        self.finish_pos = (width - 2, height - 2)
        self.generate_maze()
    
    def generate_maze(self):
        """Генерация лабиринта алгоритмом рекурсивного backtracking"""
        # Инициализация: все стены
        self.grid = [[CellType.WALL for _ in range(self.width)] for _ in range(self.height)]
        
        # Стек для backtracking
        stack = []
        
        # Начальная позиция
        start_x, start_y = 1, 1
        self.grid[start_y][start_x] = CellType.PATH
        stack.append((start_x, start_y))
        
        # Направления движения (право, низ, лево, верх)
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        
        while stack:
            current_x, current_y = stack[-1]
            
            # Найти доступные направления
            available_dirs = []
            for dx, dy in directions:
                next_x, next_y = current_x + dx, current_y + dy
                
                # Проверить границы и что клетка еще стена
                if (1 <= next_x < self.width - 1 and 
                    1 <= next_y < self.height - 1 and 
                    self.grid[next_y][next_x] == CellType.WALL):
                    available_dirs.append((dx, dy))
            
            if available_dirs:
                # Выбрать случайное направление
                dx, dy = random.choice(available_dirs)
                next_x, next_y = current_x + dx, current_y + dy
                
                # Создать проход
                self.grid[current_y + dy // 2][current_x + dx // 2] = CellType.PATH
                self.grid[next_y][next_x] = CellType.PATH
                
                # Добавить новую позицию в стек
                stack.append((next_x, next_y))
            else:
                # Backtrack
                stack.pop()
        
        # Установить старт и финиш
        self.grid[self.start_pos[1]][self.start_pos[0]] = CellType.START
        self.grid[self.finish_pos[1]][self.finish_pos[0]] = CellType.FINISH
        
        # Убедиться что финиш доступен
        self.ensure_finish_accessible()
    
    def ensure_finish_accessible(self):
        """Убедиться что финиш доступен"""
        # Простая проверка - делаем проход к финишу если он заблокирован
        fx, fy = self.finish_pos
        
        # Проверяем соседние клетки финиша
        neighbors = [(fx-1, fy), (fx+1, fy), (fx, fy-1), (fx, fy+1)]
        has_path = False
        
        for nx, ny in neighbors:
            if (0 <= nx < self.width and 0 <= ny < self.height and 
                self.grid[ny][nx] in [CellType.PATH, CellType.START]):
                has_path = True
                break
        
        # Если нет пути к финишу, создаем его
        if not has_path:
            # Создаем путь от предпоследней клетки
            if fx > 1:
                self.grid[fy][fx-1] = CellType.PATH
    
    def get_cell_type(self, x, y):
        """Получить тип клетки"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return CellType.WALL
    
    def is_valid_move(self, x, y):
        """Проверить можно ли двигаться в клетку"""
        cell_type = self.get_cell_type(x, y)
        return cell_type in [CellType.PATH, CellType.START, CellType.FINISH]
    
    def is_finish(self, x, y):
        """Проверить является ли клетка финишем"""
        return self.get_cell_type(x, y) == CellType.FINISH
    
    def get_maze_info(self):
        """Получить информацию о лабиринте"""
        return {
            'width': self.width,
            'height': self.height,
            'start': self.start_pos,
            'finish': self.finish_pos
        }
