from board import Board
from exceptions import InvalidMoveException, GameOverException, OutOfBoundsException
from game import Game
import pygame
from pygame.locals import *

class UI:
    def __init__(self):
        self.__board = Board()
        self.__game = Game(self.__board)

    def print_board(self):
        print(self.__board)

    def start_game(self):
        player_colour = input("Choose your colour: W or B : ")
        if player_colour == "W":
            computer_colour = "B"
        else: computer_colour = "W"
        print("Your colour is " + player_colour)
        print("Computer colour is " + computer_colour)
        print("Initial board")
        self.print_board()
        human_turn = True
        while True:
            if human_turn:
                human_choice = input("Do you want to capture or move? : ")
                human_turn = False
                if human_choice == 'move':
                    start_row = int(input("Start row: "))
                    start_column = int(input("Start column: "))
                    end_row = int(input("End row: "))
                    end_column = int(input("End column: "))
                    try:
                        self.__game.player_move(start_row, start_column, end_row, end_column, player_colour)
                        print("Board after player move")
                        self.print_board()
                    except (InvalidMoveException, OutOfBoundsException) as exception:
                        print(exception)
                elif human_choice == 'capture':
                    start_row = int(input("Start row: "))
                    start_column = int(input("Start column: "))
                    end_row = int(input("End row: "))
                    end_column = int(input("End column: "))
                    try:
                        self.__game.player_capture(start_row, start_column, end_row, end_column, player_colour)
                        print("Board after player capture")
                        self.print_board()
                    except (InvalidMoveException, OutOfBoundsException) as exception:
                        print(exception)
            else:
                try:
                    self.__game.computer_move(player_colour, computer_colour)
                    human_turn = True
                    print("Board after computer move")
                    self.print_board()
                except InvalidMoveException as exception:
                    print(exception)
            try:
                self.__board.game_over(player_colour, computer_colour)
            except GameOverException as exception:
                print("Game over! " , exception)

SCREEN_SIZE = 600
GRID_SIZE = 4
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
SELECT_COLOR = (0, 255, 0)
WIDTH_OF_GRID = 1
WIDTH_OF_SELECTED_CELL = 3

class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Four-Field Kono Game")
        self.board = Board()
        self.game = Game(self.board)
        self.selected_piece = None
        self.current_player = None
        self.opponent_player = None
        self.color_selected = None
        self.game_running = True

    def color_selection(self):
        self.screen.fill(GRAY)
        font = pygame.font.Font(None, 36)
        welcome_text = font.render("Welcome to Four-Field Kono!", True, BLACK)
        text = font.render("Choose your color", True, BLACK)
        self.screen.blit(welcome_text, (150, 45))
        self.screen.blit(text, (200, 100))
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(100,200,150,100))
        pygame.draw.rect(self.screen, BLACK, pygame.Rect(350,200,150,100))
        white_text = font.render("White", True, BLACK)
        black_text = font.render("Black", True, WHITE)
        self.screen.blit(white_text, (125, 230))
        self.screen.blit(black_text, (375,230))
        pygame.display.flip()

    def draw_board(self):
        self.screen.fill(GRAY)
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                rectangular_cell = pygame.Rect(column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, BLUE, rectangular_cell, WIDTH_OF_GRID)
                piece = self.board.get_piece(row, column)
                if piece == 'W':
                    pygame.draw.circle(self.screen, WHITE, rectangular_cell.center, CELL_SIZE // 6)
                elif piece == 'B':
                    pygame.draw.circle(self.screen, BLACK, rectangular_cell.center, CELL_SIZE // 6)
        if self.selected_piece:
            row,column = self.selected_piece
            rectangular_cell = pygame.Rect(column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, RED, rectangular_cell, WIDTH_OF_SELECTED_CELL)

    def handle_mouse_click(self, mouse_position):
        if not self.color_selected:
            if 100 <= mouse_position[0] <= 250 and 200 <= mouse_position[1] <= 300:
                self.current_player = 'W'
                self.opponent_player = 'B'
                self.color_selected = True
                self.start_game()
            elif 350 <= mouse_position[0] <= 500 and 200 <= mouse_position[1] <= 300:
                self.current_player = 'B'
                self.opponent_player = 'W'
                self.color_selected = True
                self.start_game()
            return
        x_coordinate, y_coordinate = mouse_position
        row = y_coordinate // CELL_SIZE
        column = x_coordinate // CELL_SIZE
        if not (0 <= row < GRID_SIZE and 0 <= column < GRID_SIZE):
            return
        if self.selected_piece:
            try:
                if abs(self.selected_piece[0] - row) == 2 or abs(self.selected_piece[1] - column) == 2:
                    self.game.player_capture(self.selected_piece[0], self.selected_piece[1], row, column, self.current_player)
                    print("Player captured")
                else:
                    self.game.player_move(self.selected_piece[0], self.selected_piece[1], row, column, self.current_player)
                    print("Player moved")
                self.selected_piece = None
                self.switch_turns()
            except (InvalidMoveException, OutOfBoundsException) as exception:
                print(exception)
        else:
            if self.board.get_piece(row, column) == self.current_player:
                self.selected_piece = (row, column)

    def switch_turns(self):
        self.current_player, self.opponent_player = self.opponent_player, self.current_player
        if self.current_player == 'B':
            self.game.computer_move(self.opponent_player, self.current_player)
            self.switch_turns()

    def check_game_over(self):
        try:
            self.board.game_over(self.current_player, self.opponent_player)
        except GameOverException as exception:
            print(exception)
            self.game_running = False

    def start_game(self):
        while self.game_running:
            self.check_game_over()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_running = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
            self.draw_board()
            pygame.display.flip()
        pygame.quit()

    def run(self):
        while not self.color_selected:
            self.color_selection()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_running = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
        self.start_game()

if __name__ == "__main__":
    gui = GUI()
    gui.run()





