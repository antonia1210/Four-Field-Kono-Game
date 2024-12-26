from texttable import Texttable

from exceptions import OutOfBoundsException, InvalidMoveException, GameOverException


class Board:
    def __init__(self, size = 4):
        self.board_size = size
        self._board = [['W', 'W', 'W', 'W'],
                       ['W', 'W', 'W', 'W'],
                       ['B', 'B', 'B', 'B'],
                       ['B', 'B', 'B', 'B'],]

    def get_piece(self, row, column):
        if not (0 <= row < self.board_size) or not (0 <= column < self.board_size):
            raise OutOfBoundsException()
        return self._board[row][column]

    def set_piece(self, row, column, marble_value):
        if not (0 <= row < self.board_size) or not (0 <= column < self.board_size):
            raise OutOfBoundsException()
        self._board[row][column] = marble_value

    def move_marble_piece(self, start_row, start_column, end_row, end_column):
        if self.get_piece(end_row, end_column) != '.':
            raise InvalidMoveException("Invalid move. Destination cell is not empty")
        if self.get_piece(end_row, end_column) == '.':
            raise InvalidMoveException("Invalid move. Cannot move an empty piece")
        if abs(start_row-end_row) + abs(start_column-end_column) != 1:
            raise InvalidMoveException("Invalid move")
        self._board[end_row][end_column] = self._board[start_row][start_column]
        self._board[start_row][start_column] = '.'

    def capture_marble_piece(self, start_row, start_column, end_row, end_column):
        middle_row = (end_row + start_row) // 2
        middle_column = (end_column + start_column) // 2
        if (start_row != end_row) and (start_column != end_column):
         raise InvalidMoveException("Invalid move. Cannot move diagonally")
        if self.get_piece(start_row, start_column) != self.get_piece(middle_row, middle_column):
            raise InvalidMoveException("Invalid move. You must jump over one of your own marbles")
        if self.get_piece(start_row, start_column) == 'W':
            if self.get_piece(end_row, end_column) == 'W':
                raise InvalidMoveException("Cell must contain the opponents marble")
        if self.get_piece(start_row, start_column) == 'B':
            if self.get_piece(end_row, end_column) == 'B':
                raise InvalidMoveException("Cell must contain the opponents marble")
        self._board[end_row][end_column] = self._board[start_row][start_column]
        self._board[start_row][start_column] = '.'

    def count_marble_pieces(self, player):
        return sum(row.count(player) for row in self._board)

    def game_over(self, player_colour, computer_colour):
        player_marble_count = self.count_marble_pieces(player_colour)
        computer_marble_count = self.count_marble_pieces(computer_colour)
        if player_marble_count == 0:
            raise GameOverException("Computer won!")
        if computer_marble_count == 0:
            raise GameOverException("You won!")

    def __str__(self):
        table = Texttable()
        header = [' '] + [str(i) for i in range(self.board_size)]
        table.header(header)
        for i in range(self.board_size):
            row = [str(i)] + self._board[i]
            table.add_row(row)
        return table.draw()


