import pygame
from colors import Colors, GameState, WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from colors import DEFAULT_MAZE_WIDTH, DEFAULT_MAZE_HEIGHT
from maze import Maze
from player import Player, CommandInterpreter
from ui import UI

class MazeGame:
    def __init__(self):
        pygame.init()
        
        # Создание окна
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Лабиринт с программированием")
        
        # Игровые параметры
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.MENU
        
        # Создание игровых объектов
        self.maze = Maze(DEFAULT_MAZE_WIDTH, DEFAULT_MAZE_HEIGHT)
        self.player = Player(*self.maze.start_pos)
        self.command_interpreter = CommandInterpreter(self.player, self.maze)
        
        # Интерфейс
        self.ui = UI(self.screen)
        self.editing_code = False  # Флаг для редактирования кода

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Обработка клавиш в зависимости от состояния игры
            if self.game_state == GameState.MENU:
                self.handle_menu_events(event)
            elif self.game_state == GameState.PLAYING:
                self.handle_playing_events(event)
            elif self.game_state == GameState.EDITING_CODE:
                self.handle_editing_code_events(event)
            elif self.game_state == GameState.EXECUTING:
                self.handle_executing_events(event)

    def handle_menu_events(self, event):
        """Обработка событий в меню"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                self.game_state = GameState.PLAYING

    def handle_playing_events(self, event):
        """Обработка событий во время игры"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self.game_state = GameState.MENU
            elif event.key == pygame.K_RETURN:
                self.game_state = GameState.EDITING_CODE
                self.editing_code = True  # Устанавливаем оба флага
            elif event.key == pygame.K_r and not self.editing_code:
                self.reset_game()
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_rects = self.ui.get_button_rects()
        
            if button_rects['execute'].collidepoint(mouse_pos):
                self.execute_code()
            elif button_rects['clear'].collidepoint(mouse_pos):
                self.ui.set_code_text("")
            elif button_rects['new_maze'].collidepoint(mouse_pos):
                self.reset_game()
            elif button_rects['code_area'].collidepoint(mouse_pos):
                self.game_state = GameState.EDITING_CODE  # Меняем состояние
                self.editing_code = True

    def handle_editing_code_events(self, event):
        """Обработка событий при редактировании кода"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.editing_code = False
                self.game_state = GameState.PLAYING
            elif event.key == pygame.K_BACKSPACE:
                self.ui.remove_character()
            elif event.key == pygame.K_RETURN:
                self.ui.add_character("\n")
            else:
                # Добавляем проверку на пустой unicode
                if event.unicode and event.unicode.isprintable():
                    self.ui.add_character(event.unicode)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_rects = self.ui.get_button_rects()
            
            if button_rects['execute'].collidepoint(mouse_pos):
                self.execute_code()
            elif button_rects['clear'].collidepoint(mouse_pos):
                self.ui.set_code_text("")
            elif button_rects['new_maze'].collidepoint(mouse_pos):
                self.reset_game()
            elif button_rects['code_area'].collidepoint(mouse_pos):
                self.editing_code = True

    def handle_executing_events(self, event):
        """Обработка событий при выполнении кода"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_state = GameState.PLAYING

    def update(self):
        """Обновление состояния игры"""
        if self.game_state == GameState.PLAYING:
            if self.player.is_at_finish(self.maze.finish_pos):
                self.game_state = GameState.GAME_OVER

    def draw(self):
        """Отрисовка элементов игры"""
        self.screen.fill(Colors.WHITE)
        
        if self.game_state == GameState.MENU:
            self.ui.draw_menu()
        elif self.game_state in [GameState.PLAYING, GameState.EDITING_CODE]:
            self.ui.draw_maze(self.maze, self.player)
            self.ui.draw_code_panel(editing_code=self.editing_code)
            self.ui.draw_buttons()
            self.ui.draw_hints()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over_screen()

        pygame.display.flip()

    def execute_code(self):
        """Выполнение пользовательского кода"""
        code = self.ui.get_code_text()
    
        # Используем интерпретатор команд вместо прямого exec
        success, message = self.command_interpreter.execute_code(code)
    
        if success:
            self.ui.set_output_text(message)
            # Проверяем, достиг ли игрок финиша
        if self.player.is_at_finish(self.maze.finish_pos):
            self.game_state = GameState.GAME_OVER
        else:
            self.ui.set_output_text(message)
    
        self.game_state = GameState.PLAYING

    def reset_game(self):
        """Сброс игры"""
        self.maze = Maze(DEFAULT_MAZE_WIDTH, DEFAULT_MAZE_HEIGHT)
        self.player = Player(*self.maze.start_pos)
        self.ui.set_code_text("")
        self.ui.set_output_text("Игра сброшена!")
        self.game_state = GameState.PLAYING

    def draw_game_over_screen(self):
        """Экран завершения игры"""
        self.screen.fill(Colors.DARK_GRAY)
        title = self.ui.font_large.render("ПОБЕДА!", True, Colors.GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        description = [
            "Вы успешно прошли лабиринт!",
            "",
            "Нажмите F1 для выхода в меню",
            "или ESC для выхода из игры."
        ]
        
        for i, line in enumerate(description):
            text = self.ui.font_medium.render(line, True, Colors.WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 300 + i * 30))
            self.screen.blit(text, text_rect)

# Запуск игры
if __name__ == "__main__":
    game = MazeGame()
    game.run()