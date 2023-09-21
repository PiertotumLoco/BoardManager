#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BoardManager.Board import Board
from BoardManager.Pieces import Queen, Pawn


def main():
    """ Main program """
    print("Bonjour Monde")
    my_board = Board(8, 8)
    queen = Queen((0, 7), True, True)
    pawn = Pawn((4, 3), False, True)
    my_board.matrix[queen.position].occupant = queen
    my_board.matrix[pawn.position].occupant = pawn
    res = queen.get_all_possible_moves_and_associated_actions(my_board)
    for pos, action in res:
        print(pos.position)
    print(my_board.matrix[queen.position].occupant.position)
    return 0


if __name__ == "__main__":
    main()
