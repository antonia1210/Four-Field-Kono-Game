class BoardException(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message

class OutOfBoundsException(BoardException):
    def __init__(self):
        super().__init__("Position is out of bounds")

class InvalidMoveException(BoardException):
    def __init__(self, message):
        super().__init__(message)

class GameOverException(BoardException):
    def __init__(self,message):
        super().__init__(message)