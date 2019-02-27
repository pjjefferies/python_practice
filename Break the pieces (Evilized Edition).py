# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 10:49:02 2019

@author: PaulJ
"""


import unittest
import numpy as np

USE_BREAK_DISPLAY = True

def break_evil_pieces(shape):
    matrix = np.array([[char for char in line]
                       for line in shape.strip('\n').splitlines()])
    rows, cols = matrix.shape

    inside_full_cell = find_internal_full_cells(matrix)
    print('matrix:\n', matrix)
    # print('inside_full_cell:', inside_full_cell)
    inside_full_groups, border_cells = (
        find_internal_full_groups(matrix, inside_full_cell))
    print('inside_full_groups:', inside_full_groups)
    print('border_cells:', border_cells)
    shape_paths = find_shape_paths(matrix, border_cells)




def find_internal_full_cells(matrix):
    internal_cells = []
    # rows, cols = matrix.shape
    for row_no in range(matrix.shape[0]):
        we_in = False
        for col_no in range(matrix.shape[1]):
            # print('row:', row_no, ', col:', col_no, ', val:',
            #       matrix[row_no, col_no], ', we_in:', we_in)
            if matrix[row_no, col_no] == '|':
                we_in = not we_in
            elif matrix[row_no, col_no] == ' ' and we_in:
                internal_cells.append([row_no, col_no])
    return internal_cells


def find_internal_full_groups(matrix, internal_cells):
    int_cells = internal_cells[:]
    internal_groups = []
    border_cells = []
    while int_cells:
        a_cell = int_cells.pop(0)
        # print('int_cells:', int_cells)
        new_group = [a_cell]
        new_group_search = [a_cell]
        group_border_cells = []
        while new_group_search:
            a_cell = new_group_search.pop(0)
            for direct in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
                test_pos = [a_cell[0] + direct[0],a_cell[1] + direct[1]]
                # print('test_pos:', test_pos)
                # if (test_pos[0] < 0 or test_pos[0]) ...
                if test_pos in int_cells:
                    # print('foo')
                    if test_pos not in new_group:
                        # print('bar')
                        new_group.append(test_pos)
                        new_group_search.append(test_pos)
                        int_cells.remove(test_pos)
            for direct in [[-1, 0], [0, 1], [1, 0], [0, -1],
                           [-1, -1], [-1, 1], [1, -1], [1, 1]]:
                test_pos = [a_cell[0] + direct[0],a_cell[1] + direct[1]]
                # print('matrix[*test_pos]:', matrix[*test_pos])
                if matrix[tuple(test_pos)] in '|-+':
                    if not test_pos in group_border_cells:
                        group_border_cells.append(test_pos)
        # print('new_group:', new_group)
        new_group = sorted(new_group, key=lambda x: (x[0], x[1]))
        group_border_cells = sorted(group_border_cells,
                                    key=lambda x: (x[0], x[1]))
        internal_groups.append(new_group)
        border_cells.append(group_border_cells)

    return internal_groups, border_cells


def find_shape_paths(matrix, border_cells):
    shapes = []
    for a_group in border_cells:
        temp_group = a_group[:]
        path = []
        path.append(temp_group.pop(0))
        path_dir = 'e'  # going CW
        while True:
            curr_cell_loc = path[-1]
            curr_cell = matrix[tuple(curr_cell_loc)]
            if path_dir == 'e':
                if curr_cell == '-':
                    next_cell_loc = [curr_cell_loc[0], curr_cell_loc[1] + 1]
                    next_cell = matrix[tuple(next_cell_loc)]
                    if next_cell not in '-+':
                        raise ValueError('Next east cell from - is not - or +')
                if curr_cell == '+':
                    for direct_no, direct in enumerate([[1, 0], [0, 1],
                                                        [-1, 0]]):
                        test_loc = [curr_cell[0] + direct[0],
                                    curr_cell[1] + direct[1]]
                        test_pos_val = matrix(tuple(test_loc))
                        if test_pos_val in '+|-':
                            next_cell_loc = test_loc
                            next_cell = test_pos_val
                            path_dir = 'sen'[direct_no]
                            break
            elif path_dir == 's':
                if curr_cell == '|':
                    next_cell_loc = [curr_cell_loc[0] + 1, curr_cell_loc[1]]
                    next_cell = matrix[tuple(next_cell_loc)]
                    if next_cell not in '|+':
                        raise ValueError(
                            'Next south cell from | isn''t | or +')
                if curr_cell == '+':
                    for direct_no, direct in enumerate([[0, -1], [1, 0],
                                                        [0, 1]]):
                        test_loc = [curr_cell[0] + direct[0],
                                    curr_cell[1] + direct[1]]
                        test_pos_val = matrix(tuple(test_loc))
                        if test_pos_val in '+|-':
                            next_cell_loc = test_loc
                            next_cell = test_pos_val
                            path_dir = 'esw'[direct_no]
                            break
            elif path_dir == 'w':
                if curr_cell == '-':
                    next_cell_loc = [curr_cell_loc[0], curr_cell_loc[1] - 1]
                    next_cell = matrix[tuple(next_cell_loc)]
                    if next_cell not in '-+':
                        raise ValueError('Next west cell from - is not - or +')
                if curr_cell == '+':
                    for direct_no, direct in enumerate([[-1, 0], [0, -1],
                                                        [1, 0]]):
                        test_loc = [curr_cell[0] + direct[0],
                                    curr_cell[1] + direct[1]]
                        test_pos_val = matrix(tuple(test_loc))
                        if test_pos_val in '+|-':
                            next_cell_loc = test_loc
                            next_cell = test_pos_val
                            path_dir = 'nws'[direct_no]
                            break
            elif path_dir == 'n':
                if curr_cell == '|':
                    next_cell_loc = [curr_cell_loc[0] - 1, curr_cell_loc[1]]
                    next_cell = matrix[tuple(next_cell_loc)]
                    if next_cell not in '|+':
                        raise ValueError(
                            'Next north cell from | isn''t | or +')
                if curr_cell == '+':
                    for direct_no, direct in enumerate([[0, 1], [-1, 0],
                                                        [0, -1]]):
                        test_loc = [curr_cell[0] + direct[0],
                                    curr_cell[1] + direct[1]]
                        test_pos_val = matrix(tuple(test_loc))
                        if test_pos_val in '+|-':
                            next_cell_loc = test_loc
                            next_cell = test_pos_val
                            path_dir = 'enw'[direct_no]
                            break
            else:
                raise ValueError("We're lost!")
            path.append(next_cell_loc)
            temp_group.remove(next_cell_loc)
            if path[0] == path[-1]:
                path = path[:-1]
                break



class TestMethods(unittest.TestCase):

    # tests = {1: [(9, 16), lambda: game.size(), ]}

    def test_basic(self):
        # Test 1 - Simple shape
        print('Test 1: ', end='')
        shape = """
+----------+
|          |
|          |
|          |
+----------+
|          |
|          |
+----------+
""".strip('\n')
        answer = expected = ["""
+----------+
|          |
|          |
|          |
+----------+
""".strip('\n'), """
+----------+
|          |
|          |
+----------+
""".strip('\n'), ]
        result = break_evil_pieces(shape)
        self.assertEqual(result, answer)
        print('correct!')

        # Test 2 - 3 Boxes
        print('Test 2: ', end='')
        shape = """
+------------+
|            |
|            |
|            |
+------+-----+
|      |     |
|      |     |
+------+-----+
""".strip('\n')

        answer = ["""
+------------+
|            |
|            |
|            |
+------------+
""".strip('\n'), """
+------+
|      |
|      |
+------+
""".strip('\n'), """
+-----+
|     |
|     |
+-----+
""".strip('\n'),]
        result = break_evil_pieces(shape)
        self.assertEqual(result, answer)
        print('correct!')

        # Test 3 - Lego stuff
        print('Test 3: ', end='')
        shape = """
+-------------------+--+
|                   |  |
|                   |  |
|  +----------------+  |
|  |                   |
|  |                   |
+--+-------------------+
""".strip('\n')
        answer = ["""
+-------------------+
|                   |
|                   |
|  +----------------+
|  |
|  |
+--+
""".strip('\n'), """
                 +--+
                 |  |
                 |  |
+----------------+  |
|                   |
|                   |
+-------------------+
""".strip('\n'),]
        result = break_evil_pieces(shape)
        self.assertEqual(result, answer)
        print('correct!')

        # Test 4 - Piece of cake! (check for irrelevant spaces)
        print('Test 4: ', end='')
        shape = """
                           
                           
           +-+             
           | |             
         +-+-+-+           
         |     |           
      +--+-----+--+        
      |           |        
   +--+-----------+--+     
   |                 |     
   +-----------------+     
                           
                           
""".strip('\n')
        answer = ["""
+-+
| |
+-+
""".strip('\n'), """
+-----+
|     |
+-----+
""".strip('\n'), """
+-----------+
|           |
+-----------+
""".strip('\n'), """
+-----------------+
|                 |
+-----------------+
""".strip('\n'), ]
        result = break_evil_pieces(shape)
        self.assertEqual(result, answer)
        print('correct!')

        # Test 5 - Horseshoe (shapes are not always rectangles!)
        print('Test 5: ', end='')
        shape = """
+-----------------+
|                 |
|   +-------------+
|   |
|   |
|   |
|   +-------------+
|                 |
|                 |
+-----------------+
""".strip('\n')
        answer = [shape]
        result = break_evil_pieces(shape)
        self.assertEqual(result, answer)
        print('correct!')

        # Test 6 - Warming up
        print('Test 6: ', end='')
        shape = """
+------------+
|            |
|            |
|            |
+------++----+
|      ||    |
|      ||    |
+------++----+
""".strip('\n')

        answer = ["""
+------------+
|            |
|            |
|            |
+------------+
""".strip('\n'), """
+------+
|      |
|      |
+------+
""".strip('\n'), """
+----+
|    |
|    |
+----+
""".strip('\n'), """
++
||
||
++
""".strip('\n'),]
        result = break_evil_pieces(shape)
        self.assertEqual(result, answer)
        print('correct!')

        # Test 7 - Don't forget the eggs! (you'll understand later...)
        print('Test 7: ', end='')
        shape = """
++
++
""".strip('\n')
        expected = [shape]
        result = break_evil_pieces(shape)
        self.assertEqual(result, answer)
        print('correct!')


if __name__ == '__main__':
    unittest.main()

"""
Result:

"""
