"""
Модуль игрока и интерпретатора команд
"""

class Player:
    """Класс игрока в лабиринте"""
    
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.moves_count = 0
        self.move_history = []
    
    def reset_position(self):
        """Сбросить позицию игрока на стартовую"""
        self.x = self.start_x
        self.y = self.start_y
        self.moves_count = 0
        self.move_history.clear()
    
    def set_start_position(self, x, y):
        """Установить новую стартовую позицию"""
        self.start_x = x
        self.start_y = y
        self.reset_position()
    
    def move_to(self, new_x, new_y):
        """Переместить игрока в новую позицию"""
        old_pos = (self.x, self.y)
        self.x = new_x
        self.y = new_y
        self.moves_count += 1
        self.move_history.append((old_pos, (new_x, new_y)))
    
    def get_position(self):
        """Получить текущую позицию"""
        return (self.x, self.y)
    
    def get_stats(self):
        """Получить статистику игрока"""
        return {
            'position': (self.x, self.y),
            'moves': self.moves_count,
            'start': (self.start_x, self.start_y)
        }
    
    def is_at_finish(self, finish_pos: tuple):
        """Проверить, находится ли игрок в финальной позиции"""
        return finish_pos == (self.x, self.y)



class CommandInterpreter:
    """Интерпретатор команд для управления игроком"""
    
    def __init__(self, player, maze):
        self.player = player
        self.maze = maze
        self.execution_log = []
        self.error_log = []
    
    def clear_logs(self):
        """Очистить логи выполнения"""
        self.execution_log.clear()
        self.error_log.clear()
    
    def log_move(self, command, success, message=""):
        """Записать движение в лог"""
        self.execution_log.append({
            'command': command,
            'success': success,
            'message': message,
            'position': self.player.get_position()
        })
    
    def move_up(self):
        """Движение вверх"""
        new_x, new_y = self.player.x, self.player.y - 1
        if self.maze.is_valid_move(new_x, new_y):
            self.player.move_to(new_x, new_y)
            self.log_move("move_up()", True, f"Перемещение в ({new_x}, {new_y})")
            return True
        else:
            self.log_move("move_up()", False, "Нельзя двигаться вверх - стена!")
            return False
    
    def move_down(self):
        """Движение вниз"""
        new_x, new_y = self.player.x, self.player.y + 1
        if self.maze.is_valid_move(new_x, new_y):
            self.player.move_to(new_x, new_y)
            self.log_move("move_down()", True, f"Перемещение в ({new_x}, {new_y})")
            return True
        else:
            self.log_move("move_down()", False, "Нельзя двигаться вниз - стена!")
            return False
    
    def move_left(self):
        """Движение влево"""
        new_x, new_y = self.player.x - 1, self.player.y
        if self.maze.is_valid_move(new_x, new_y):
            self.player.move_to(new_x, new_y)
            self.log_move("move_left()", True, f"Перемещение в ({new_x}, {new_y})")
            return True
        else:
            self.log_move("move_left()", False, "Нельзя двигаться влево - стена!")
            return False
    
    def move_right(self):
        """Движение вправо"""
        new_x, new_y = self.player.x + 1, self.player.y
        if self.maze.is_valid_move(new_x, new_y):
            self.player.move_to(new_x, new_y)
            self.log_move("move_right()", True, f"Перемещение в ({new_x}, {new_y})")
            return True
        else:
            self.log_move("move_right()", False, "Нельзя двигаться вправо - стена!")
            return False
    
    def get_position(self):
        """Получить текущую позицию игрока"""
        return self.player.get_position()
    
    def is_at_finish(self):
        """Проверить находится ли игрок на финише"""
        x, y = self.player.get_position()
        return self.maze.is_finish(x, y)
    
    def execute_code(self, code):
        """Выполнить код пользователя"""
        self.clear_logs()
        
        try:
            # Создаем безопасный контекст для выполнения
            safe_globals = {
                'move_up': self.move_up,
                'move_down': self.move_down,
                'move_left': self.move_left,
                'move_right': self.move_right,
                'get_position': self.get_position,
                'is_at_finish': self.is_at_finish,
                '__builtins__': {
                    'range': range,
                    'len': len,
                    'print': print,
                    'for': 'for',  # Разрешаем циклы
                    'if': 'if',    # Разрешаем условия
                    'while': 'while'
                }
            }
            
            # Выполняем код
            exec(code, safe_globals)
            
            # Проверяем победу
            if self.is_at_finish():
                self.log_move("FINISH", True, "🎉 Поздравляем! Вы достигли финиша!")
            
            return True, self.get_execution_summary()
            
        except Exception as e:
            error_msg = f"Ошибка выполнения: {str(e)}"
            self.error_log.append(error_msg)
            return False, error_msg
    
    def get_execution_summary(self):
        """Получить сводку выполнения"""
        if not self.execution_log:
            return "Код выполнен, но команды движения не найдены."
        
        summary = []
        summary.append(f"Выполнено команд: {len(self.execution_log)}")
        summary.append(f"Общее количество ходов: {self.player.moves_count}")
        summary.append(f"Текущая позиция: {self.player.get_position()}")
        
        # Последние несколько команд
        recent_commands = self.execution_log[-5:]
        summary.append("\nПоследние команды:")
        for cmd in recent_commands:
            status = "✓" if cmd['success'] else "✗"
            summary.append(f"{status} {cmd['command']}: {cmd['message']}")
        
        return "\n".join(summary)
