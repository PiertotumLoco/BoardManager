import operator
from collections import namedtuple
from enum import Enum
from BoardManager.Board import Position

Move = namedtuple("Move", ["direction", "depth", "conditions"])


class RelativeMovement(namedtuple('RelativeMovement', ['vertical_displacement', 'horizontal_displacement'])):
    """
    Namedtuple representing a displacement vector. __add__ and __mul__ overload to mimic 2D array operations.
    """
    def __add__(self, other):
        if not isinstance(other, RelativeMovement):
            raise ValueError("Addition requires tuples of the same length")
        return RelativeMovement(self.vertical_displacement + other.vertical_displacement,
                                self.horizontal_displacement + other.horizontal_displacement)

    def __mul__(self, other):
        return RelativeMovement(other * self.vertical_displacement, other * self.horizontal_displacement)

    __rmul__ = __mul__


MOVE_NORTH = RelativeMovement(0, 1)
MOVE_SOUTH = RelativeMovement(0, -1)
MOVE_WEST = RelativeMovement(-1, 0)
MOVE_EAST = RelativeMovement(1, 0)
MOVE_NORTHEAST = RelativeMovement(1, 1)
MOVE_NORTHWEST = RelativeMovement(-1, 1)
MOVE_SOUTHEAST = RelativeMovement(1, -1)
MOVE_SOUTHWEST = RelativeMovement(-1, -1)


class WeirdMovement(RelativeMovement):
    pass


MOVE_KNIGHT = 9
MOVE_CASTLING = 10


class Action(Enum):
    NO_ACTION = 0
    KILL = 1
    PROMOTE = 2
    MOVE_CASTLE_TO = 3


class Condition(Enum):
    NO_CONDITION = 0
    NEVER_MOVED = 1
    CANNOT_KILL = 2
    MUST_KILL = 3
    CLEAR_PATH = 4
    # TODO: Castling condition


class PositionOutOfBoardError(Exception):
    pass


class Piece:
    def __init__(self, position, color, is_alive, authorized_moves, has_moved=False):
        self.isAlive = is_alive
        self.position = Position(*position)
        self.color = color  # True is white
        self.authorized_moves = authorized_moves  # child classes implement the authorized moves
        self.hasMoved = has_moved

    # @staticmethod
    # def obsolete_rotate_board_90_degrees_counterclockwise(board, number_of_rotation=1):
    #     # https://stackoverflow.com/a/8421412
    #     rotated_board = board
    #     for _ in range(number_of_rotation):
    #         rotated_board = list(reversed(list(zip(*rotated_board))))
    #     return rotated_board

    def get_relative_destination(self, absolute_destination):
        # Position is a namedTuple and takes exactly 2 arguments (cannot be initialized with a tuple
        # Hence the unpacking star (*) in front of map
        return Position(*map(operator.sub, absolute_destination, self.position))

    @staticmethod
    def get_absolute_destination(position, relative_destination):
        return Position(*map(operator.add, relative_destination, position))

    def kill_self(self):
        self.isAlive = False

    def get_squares_accessible_in_line(self, board, move):
        accessible_squares = set()
        if Condition.NEVER_MOVED in move.conditions and self.hasMoved is True:
            return accessible_squares
        next_position = self.position
        for current_depth in range(move.depth):
            try:
                next_position = self.get_absolute_destination(next_position, move.direction)
                if any(value < 0 or next_position.file >= board.width or next_position.rank >= board.height
                       for value in next_position):
                    raise PositionOutOfBoardError("{} out of board".format(next_position))
            except PositionOutOfBoardError as error:
                print(error)
                break
            square_to_evaluate = board.matrix[next_position]
            # empty square
            if square_to_evaluate.occupant is None:
                if Condition.MUST_KILL in move.conditions:
                    break
                else:
                    accessible_squares.add((square_to_evaluate, Action.NO_ACTION))
                    continue

            # occupied square
            elif Condition.CANNOT_KILL in move.conditions:
                if Condition.CLEAR_PATH in move.conditions:
                    break
                else:
                    continue
            elif square_to_evaluate.occupant.color is not self.color:
                accessible_squares.add((square_to_evaluate, Action.KILL))

        return accessible_squares

    # @staticmethod
    # def obsolete_rotate_coordinates_90_degrees_counterclockwise(coordinates, number_of_rotation):
    #     # doesn't work for non-standard board size
    #     (x, y) = coordinates
    #     for _ in range(number_of_rotation):
    #         (x, y) = (8 - y, x)
    #     return Position(x, y)

    def get_all_possible_moves_and_associated_actions(self, board):
        all_moves_and_actions = []
        for move in self.authorized_moves:
            all_moves_and_actions += self.get_squares_accessible_in_line(board, move)

        return all_moves_and_actions


class King(Piece):
    def __init__(self, position, color, is_alive):
        self.authorized_moves = {Move(MOVE_NORTH, depth=1, conditions=frozenset([])),
                                 Move(MOVE_SOUTH, depth=1, conditions=frozenset([])),
                                 Move(MOVE_EAST, depth=1, conditions=frozenset([])),
                                 Move(MOVE_WEST, depth=1, conditions=frozenset([])),
                                 Move(MOVE_NORTHEAST, depth=1, conditions=frozenset([])),
                                 Move(MOVE_SOUTHEAST, depth=1, conditions=frozenset([])),
                                 Move(MOVE_NORTHWEST, depth=1, conditions=frozenset([])),
                                 Move(MOVE_SOUTHWEST, depth=1, conditions=frozenset([]))
                                 }

        super().__init__(position, color, is_alive, self.authorized_moves)


class Queen(Piece):
    def __init__(self, position, color, is_alive):
        self.authorized_moves = {Move(MOVE_NORTH, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_SOUTH, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_EAST, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_WEST, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_NORTHEAST, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_SOUTHEAST, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_NORTHWEST, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_SOUTHWEST, depth=8, conditions=frozenset([Condition.CLEAR_PATH]))
                                 }

        super().__init__(position, color, is_alive, self.authorized_moves)


class Rook(Piece):
    def __init__(self, position, color, is_alive):
        self.authorized_moves = {Move(MOVE_NORTH, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_SOUTH, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_EAST, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_WEST, depth=8, conditions=frozenset([Condition.CLEAR_PATH]))
                                 }

        super().__init__(position, color, is_alive, self.authorized_moves)


class Bishop(Piece):
    def __init__(self, position, color, is_alive):
        self.authorized_moves = {Move(MOVE_NORTHEAST, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_SOUTHEAST, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_NORTHWEST, depth=8, conditions=frozenset([Condition.CLEAR_PATH])),
                                 Move(MOVE_SOUTHWEST, depth=8, conditions=frozenset([Condition.CLEAR_PATH]))
                                 }

        super().__init__(position, color, is_alive, self.authorized_moves)


class Knight(Piece):
    """
    Knight Piece.

    Can move two squares forward or backward and one square to the side, or two squares to the side and one square
    forward or backward, if destination is empty or occupied by opponent.
    """
    def __init__(self, position, color, is_alive):
        self.authorized_moves = {Move(2 * MOVE_NORTH + MOVE_EAST, depth=1, conditions=frozenset([])),
                                 Move(2 * MOVE_NORTH + MOVE_WEST, depth=1, conditions=frozenset([])),
                                 Move(2 * MOVE_SOUTH + MOVE_EAST, depth=1, conditions=frozenset([])),
                                 Move(2 * MOVE_SOUTH + MOVE_WEST, depth=1, conditions=frozenset([])),
                                 Move(2 * MOVE_EAST + MOVE_NORTH, depth=1, conditions=frozenset([])),
                                 Move(2 * MOVE_EAST + MOVE_SOUTH, depth=1, conditions=frozenset([])),
                                 Move(2 * MOVE_WEST + MOVE_NORTH, depth=1, conditions=frozenset([])),
                                 Move(2 * MOVE_WEST + MOVE_SOUTH, depth=1, conditions=frozenset([]))
                                 }

        super().__init__(position, color, is_alive, self.authorized_moves)


class Pawn(Piece):
    """
    Pawn piece.

    Can move 1 up if destination is empty
    Can move 2 up if 1 up and 2 up are empty and self never moved before
    can move 1 diagonally if destination taken by opposite color
    """

    def __init__(self, position, color, is_alive):
        if color is True:
            up = MOVE_NORTH
        else:
            up = MOVE_SOUTH
        self.authorized_moves = {Move(up, depth=1, conditions=frozenset([Condition.CANNOT_KILL])),
                                 Move(2 * up, 1, frozenset([Condition.CLEAR_PATH,
                                                            Condition.CANNOT_KILL,
                                                            Condition.NEVER_MOVED])),
                                 Move(up + MOVE_EAST, 1, frozenset([Condition.MUST_KILL])),
                                 Move(up + MOVE_WEST, 1, frozenset([Condition.MUST_KILL]))}

        super().__init__(position, color, is_alive, self.authorized_moves)
