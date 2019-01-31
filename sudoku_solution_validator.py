# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 11:03:21 2019

@author: PaulJ
"""


def sudoku_solution_validator(board):
    def validate_nine_unique_digits(a_seq):
        return sorted(a_seq) == list(range(1, 10))

    # check rows
    for a_row_seq in board:
        if not validate_nine_unique_digits(a_row_seq):
            return False

    # check columns
    for a_col_no in range(9):
        a_col_seq = [board[row][a_col_no] for row in range(9)]
        if not validate_nine_unique_digits(a_col_seq):
            return False

    # check quadrants
    for a_horiz_quad in range(3):
        for a_vert_quad in range(3):
            a_quad_seq = [board[3*a_vert_quad+row][3*a_horiz_quad+col]
                          for row in range(3) for col in range(3)]
        if not validate_nine_unique_digits(a_quad_seq):
            return False

    return True
