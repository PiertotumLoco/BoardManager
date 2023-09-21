from BoardManager.Board import Board
from BoardManager.Pieces import King


def test_king():
    my_board = Board(width=8, height=8)
    my_king = King((0, 0), True, True)
    moves = my_king.get_all_possible_moves_and_associated_actions(my_board)
    assert len(moves) is 3
