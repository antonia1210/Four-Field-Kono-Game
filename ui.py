from board import Board
from exceptions import InvalidMoveException, GameOverException, OutOfBoundsException
from game import Game

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
                    self.__game.computer_move(computer_colour)
                    human_turn = True
                    print("Board after computer move")
                    self.print_board()
                except InvalidMoveException as exception:
                    print(exception)
            try:
                self.__board.game_over()
            except GameOverException as exception:
                print(exception)

if __name__ == "__main__":
    ui = UI()
    ui.start_game()



