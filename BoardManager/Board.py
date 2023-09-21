from BoardManager.TListfile import TList
from collections import namedtuple

Position = namedtuple('Position', ['file', 'rank'])  # file = column, rank = row


class Square:
    def __init__(self, position, occupant):
        self.occupant = occupant
        self.position = Position(*position)


class Board:
    ACTIVE_BOARD_WIDTH = 8
    INACTIVE_BOARD_WIDTH = 4
    BOARD_HEIGHT = 8

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # the board is represented by a row*line 2d matrix of squares
        # TList can be indexed with tuples, homogenous with a piece position
        self.matrix = TList(
            [
                [Square((file, rank), None)for rank in range(self.height)]
                for file in range(self.width)
            ]
        )
