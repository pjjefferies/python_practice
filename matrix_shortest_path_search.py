# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 22:30:00 2019

@author: PaulJ
"""

import unittest
from time import time
# import copy
import numpy as np

NEIGHBOR_DELTA_TO_VISIT = [(row, col, (row**2 + col**2)**0.5)
                           for col in [-1, 0, 1]
                           for row in [-1, 0, 1]
                           if (row != 0 or col != 0)]
ROW = 0
COL = 1
DIST = 2
MIN_DIST = 0
PATH = 1


def wire_DHD_SG1_python(existingWires):
    rows = existingWires.strip('\n').split('\n')
    matrix = [list(row) for row in rows]
    rows = len(matrix)
    cols = len(matrix[0])
    start_row, start_col = [(row_no, col_no) for col_no in range(cols)
                            for row_no in range(rows)
                            if matrix[row_no][col_no] == 'S'][0]
    goal_row, goal_col = [(row_no, col_no) for col_no in range(cols)
                          for row_no in range(rows)
                          if matrix[row_no][col_no] == 'G'][0]
    cells_to_visit = [[start_row, start_col]]
    cells_min_dist = []
    cells_min_path = []

    for a_row_no in range(rows):
        temp_row_path = []
        for a_col_no in range(cols):
            temp_row_path.append([])
        temp_row_dist = [1e6] * cols
        cells_min_dist.append(temp_row_dist)
        cells_min_path.append(temp_row_path)
    cells_min_dist[start_row][start_col] = 0

    while cells_to_visit:
        start_cell = cells_to_visit.pop(0)
        for a_neigh_delta in NEIGHBOR_DELTA_TO_VISIT:
            new_neigh = [start_cell[ROW]+a_neigh_delta[ROW],
                         start_cell[COL]+a_neigh_delta[COL]]
            if (new_neigh[ROW] < 0 or new_neigh[ROW] >= rows or
                    new_neigh[COL] < 0 or new_neigh[COL] >= cols):
                continue
            if matrix[new_neigh[ROW]][new_neigh[COL]] == 'X':
                continue
            new_dist_temp = (cells_min_dist[start_cell[ROW]][start_cell[COL]] +
                             a_neigh_delta[DIST])
            old_dist_temp = cells_min_dist[new_neigh[ROW]][new_neigh[COL]]
            if (new_dist_temp < old_dist_temp):
                cells_min_dist[new_neigh[ROW]][new_neigh[COL]] = new_dist_temp
                new_path = (cells_min_path[start_cell[ROW]][start_cell[COL]] +
                            [start_cell])
                cells_min_path[new_neigh[ROW]][new_neigh[COL]] = new_path
                if new_neigh != [goal_row, goal_col]:
                    cells_to_visit.append(new_neigh)

    result_matrix = [row[:] for row in matrix]
    if cells_min_path[goal_row][goal_col]:
        for row, col in cells_min_path[goal_row][goal_col][1:]:
            result_matrix[row][col] = 'P'
        return '\n'.join([''.join(row) for row in result_matrix])
    else:
        return "Oh for crying out loud..."



def wire_DHD_SG1_numpy(existingWires):
    matrix = np.array([[char for char in line]
                       for line in existingWires.strip('\n').splitlines()])
    rows, cols = matrix.shape
    start = list(zip(*np.where(matrix == 'S')))[0]
    goal_row, goal_col = list(zip(*np.where(matrix == 'G')))[0]

    cells_to_visit = [start]
    cells_min_dist = np.full((rows, cols), 1e6)
    cells_min_path = np.full((rows, cols), None)

    cells_min_dist[start] = 0
    cells_min_path[start] = []
    cells_min_path[goal_row][goal_col] = []

    while cells_to_visit:
        start_cell = cells_to_visit.pop(0)
        for a_neigh_delta in NEIGHBOR_DELTA_TO_VISIT:
            new_neigh = [start_cell[ROW]+a_neigh_delta[ROW],
                         start_cell[COL]+a_neigh_delta[COL]]
            if (new_neigh[ROW] < 0 or new_neigh[ROW] >= rows or
                    new_neigh[COL] < 0 or new_neigh[COL] >= cols):
                continue
            if matrix[new_neigh[ROW], new_neigh[COL]] == 'X':
                continue
            new_dist_temp = (cells_min_dist[start_cell[ROW], start_cell[COL]] +
                             a_neigh_delta[DIST])
            old_dist_temp = cells_min_dist[new_neigh[ROW], new_neigh[COL]]
            if (new_dist_temp < old_dist_temp):
                cells_min_dist[new_neigh[ROW], new_neigh[COL]] = new_dist_temp
                cells_min_path[new_neigh[ROW], new_neigh[COL]] = (
                    cells_min_path[start_cell[ROW], start_cell[COL]] +
                    [start_cell])
                if new_neigh != [goal_row, goal_col]:
                    cells_to_visit.append(new_neigh)

    result_matrix = np.array([row[:] for row in matrix])
    if len(cells_min_path[goal_row][goal_col]) > 0:
        for row, col in cells_min_path[goal_row][goal_col][1:]:
            result_matrix[row, col] = 'P'
        return '\n'.join([''.join(row) for row in result_matrix])
    else:
        return "Oh for crying out loud..."


def wire_DHD_SG1(existingWires):
    # return wire_DHD_SG1_python(existingWires)
    return wire_DHD_SG1_numpy(existingWires)


class TestMethods(unittest.TestCase):

    tests = {'\nSX.\nXX.\n..G'.strip('\n'): 'Oh for crying out loud...',
             'SX.\nX..\nXXG'.strip('\n'): 'SX.\nXP.\nXXG'.strip('\n'),
             '.S.\n...\n.G.': '.S.\n.P.\n.G.',
             '...\nS.G\n...': '...\nSPG\n...',
             '...\nSG.\n...': '...\nSG.\n...',
             '.S...\nXXX..\n.X.XX\n..X..\nG...X':
                 '.SP..\nXXXP.\n.XPXX\n.PX..\nG...X',
             'XX.S.XXX..\nXXXX.X..XX\n...X.XX...\nXX...XXX.X\n....XXX...\nXXXX...XXX\nX...XX...X\nX...X...XX\nXXXXXXXX.X\nG........X':
                 'XX.S.XXX..\nXXXXPX..XX\n...XPXX...\nXX.P.XXX.X\n...PXXX...\nXXXXPP.XXX\nX...XXP..X\nX...X..PXX\nXXXXXXXXPX\nGPPPPPPP.X',
             }

    def test_basic(self):
        python_start_time = time()
        print('Python Tests')
        for starting_map in self.tests:
            answer_map = self.tests[starting_map]
            result = wire_DHD_SG1_python(starting_map)
            if result != answer_map:
                print('\nwrong: starting_map:', starting_map, ', answer_map:',
                      answer_map, ', result:', result)
            else:
                # print('\ncorrect!')
                pass
            self.assertEqual(result, answer_map)
        python_duration = time() - python_start_time

        numpy_start_time = time()
        print('numpy Tests')
        for starting_map in self.tests:
            answer_map = self.tests[starting_map]
            result = wire_DHD_SG1_numpy(starting_map)
            if result != answer_map:
                print('\nwrong: starting_map:', starting_map, ', answer_map:',
                      answer_map, ', result:', result)
            else:
                # print('\ncorrect!')
                pass
            self.assertEqual(result, answer_map)
        numpy_duration = time() - numpy_start_time

        print('Python Time:', round(python_duration, 4))
        print('Numpy  Time:', round(numpy_duration, 4))


if __name__ == '__main__':
    unittest.main()

"""
Result:
    Python Time: 0.001
    Numpy  Time: 0.003
"""