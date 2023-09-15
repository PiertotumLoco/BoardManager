#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Board import Board
import Pieces


def main():
    """ Main program """
    print("Bonjour Monde")
    my_board = Board(8, 8)
    pawn1 = Pieces.Queen((0, 7), True, True)
    pawn2 = Pieces.Pawn((4, 3), False, True)
    my_board.matrix[pawn1.position].occupant = pawn1
    my_board.matrix[pawn2.position].occupant = pawn2
    res = pawn1.get_all_possible_moves_and_associated_actions(my_board)
    for pos, action in res:
        print(pos.position)
    print(my_board.matrix[pawn1.position].occupant.position)
    return 0


if __name__ == "__main__":
    main()
