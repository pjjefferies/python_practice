# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 11:04:30 2019

@author: PaulJ
"""


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]

    return sum([top_row_val * (-1)**(col_no) *
               determinant([a_row[:col_no] + a_row[col_no + 1:]
                           for a_row in matrix[1:]])
               for col_no, top_row_val in enumerate(matrix[0])])
