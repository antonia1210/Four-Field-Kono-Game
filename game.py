from exceptions import InvalidMoveException, GameOverException, OutOfBoundsException
from random import randint

class Game:
    def __init__(self, board ):
        self.__board = board

    def computer_move(self, player_colour, computer_colour):
        try:
            self.__board.game_over(player_colour, computer_colour)
            start_row = randint(0, self.__board.board_size - 1)
            start_column = randint(0, self.__board.board_size - 1)
            if self.__board.get_piece(start_row, start_column) == computer_colour:
                end_row = randint(0, self.__board.board_size - 1)
                end_column = randint(0, self.__board.board_size - 1)
                if self.__board.get_piece(end_row, end_column) == '.':
                        self.__board.move_marble_piece(start_row, start_column, end_row, end_column)
                elif self.__board.get_piece(end_row, end_column) != computer_colour:
                    self.__board.capture_marble_piece(start_row, start_column, end_row, end_column)
                else:
                    self.computer_move(player_colour, computer_colour)
            else:
                self.computer_move(player_colour, computer_colour)
        except (InvalidMoveException, OutOfBoundsException):
            self.computer_move(player_colour, computer_colour)
        except GameOverException:
            return


    def player_move(self, start_row, start_column, end_row, end_column, player_colour):
        if self.__board.get_piece(start_row, start_column) == player_colour:
            self.__board.move_marble_piece(start_row, start_column, end_row, end_column)
        else:
            raise InvalidMoveException("Can't move your opponents piece")

    def player_capture(self, start_row, start_column, end_row, end_column, player_colour):
        if self.__board.get_piece(start_row, start_column) == player_colour:
            self.__board.capture_marble_piece(start_row, start_column, end_row, end_column)
        else:
            raise InvalidMoveException("Can't move your opponents piece")