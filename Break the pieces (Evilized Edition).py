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

    inside_full_cells = find_internal_full_cells(matrix)
    print('matrix:\n', matrix)
    print('inside_full_cells:', inside_full_cells)

    inside_full_groups, border_cells = (
        find_internal_full_groups(matrix, inside_full_cells))
    print('inside_full_groups:', inside_full_groups)
    print('border_cells:', border_cells)

    inside_half_cells = find_internal_half_cells(matrix)
    print('inside_half_cells:', inside_full_cells)

    inside_groups, border_cells = (
        find_internal_full_groups(matrix,
                                  inside_full_cells,
                                  inside_half_cells,
                                  inside_full_groups,
                                  border_cells))
    print('inside_groups:', inside_groups)
    print('border_cells:', border_cells)

    border_cells = crop_shift_cells(border_cells)




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
            # Look for connected open space
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
            # Look for surrounding border
            for direct in [[-1, 0], [0, 1], [1, 0], [0, -1],
                           [-1, -1], [-1, 1], [1, -1], [1, 1]]:
                test_x, test_y = a_cell[0] + direct[0], a_cell[1] + direct[1]
                test_pos = [test_y, test_x, matrix[test_y, test_x]]
                # print('matrix[*test_pos]:', matrix[*test_pos])
                if test_pos[2] in '|-+':
                    if test_pos not in group_border_cells:
                        group_border_cells.append(test_pos)
        # print('new_group:', new_group)
        new_group = sorted(new_group, key=lambda x: (x[0], x[1]))
        group_border_cells = sorted(group_border_cells,
                                    key=lambda x: (x[0], x[1]))
        internal_groups.append(new_group)
        border_cells.append(group_border_cells)

    return internal_groups, border_cells


def find_internal_half_cells(matrix):
    internal_half_cells = []
    # rows, cols = matrix.shape
    # Search for vertical, narrow passageways
    rows, cols = matrix.shape
    for row_no in range(rows):
        next_row_no = row_no + 1
        for col_no in range(cols):
            next_col_no = col_no + 1
            # Search for vertical, narrow passageways
            if next_row_no < rows:
                if ((matrix[row_no, col_no] in ('|', '+') and
                     matrix[row_no, next_col_no] == '|') or
                    (matrix[row_no, next_col_no] in ('|', '+') and
                     matrix[row_no, col_no] == '|')):
                    internal_half_cells.append([row_no, col_no + 0.5])
            # Search for horiz, narrow passageways
            if nex_col_no < cols:
                if ((matrix[row_no, col_no] in ('-', '+') and
                     matrix[next_row_no, col_no] == '-') or
                    (matrix[next_row_no, col_no] in ('-', '+') and
                     matrix[row_no, col_no] == '-')):
                    internal_half_cells.append([row_no + 0.5, col_no])
                # Search for single half-cell box ++\n++
                if next_row_no < rows:
                    if (matrix[row_no, col_no] == '+' and
                        matrix[row_no, next_col_no] == '+' and
                        matrix[next_row_no, col_no] == '+' and
                            matrix[next_row_no, next_col_no] == '+'):
                        internal_half_cells.append([row_no + 0.5,
                                                    col_no + 0.5])
    return internal_half_cells


def find_internal_half_groups(matrix,
                              full_cells,
                              int_half_cells,
                              in_full_groups,
                              border_cells):
    half_cells = int_half_cells[:]
    internal_groups = []
    new_inter_groups = in_full_groups[:]
    new_border_cells = border_cells[:]
    while half_cells:
        a_cell = half_cells.pop(0)
        # print('int_cells:', int_cells)
        new_group = [a_cell]
        full_groups_attached = []
        new_group_search = [a_cell]
        group_border_cells = []
        while new_group_search:
            a_cell = new_group_search.pop(0)
            # Check for single quarter cell first
            if (a_cell[0] != int(a_cell[0])) and (a_cell[1] != int(a_cell[0])):
                for direct in [[-0.5, -0.5], [-0.5, 0.5],
                               [0.5, -0.5], [0.5, 0.5]]:
                    test_x, test_y = (a_cell[0] + direct[0],
                                      a_cell[1] + direct[1])
                    test_pos = [test_y, test_x, matrix[test_y, test_x]]
                    group_border_cells.append(test_pos)
            # Search vertically
            elif a_cell[0] == int(a_cell[0]):
                # Look for connected half-cell spaces
                for direct in [[-1, 0], [1, 0],
                               [-0.5, -0.5], [-0.5, 0.5],
                               [0.5, -0.5], [0.5, 0.5]]:
                    test_pos = [a_cell[0] + direct[0], a_cell[1] + direct[1]]
                    # print('test_pos:', test_pos)
                    # if (test_pos[0] < 0 or test_pos[0]) ...
                    if test_pos in half_cells:
                        # print('foo')
                        if test_pos not in new_group:
                            # print('bar')
                            new_group.append(test_pos)
                            new_group_search.append(test_pos)
                            half_cells.remove(test_pos)
                # Look for connected full-cell spaces
                for direct in [[-1, -0.5], [-1, 0.5], [1, -0.5], [1, 0.5]]:
                    test_pos = [a_cell[0] + direct[0],
                                int(round(a_cell[1] + direct[1], 0))]
                    index = [i for i, s in enumerate(new_inter_groups)
                             if test_pos in s]
                    full_group = index[0] if index else -1
                    if full_group not in full_groups_attached:
                        full_groups_attached.append(full_group)
                # Look for surrounding border
                for direct in [[0, -0.5], [0, 0.5]]:
                    test_x, test_y = (a_cell[0] + direct[0],
                                      int(round(a_cell[1] + direct[1], 0)))
                    test_pos = [test_y, test_x, matrix[test_y, test_x]]
                    # print('matrix[*test_pos]:', matrix[*test_pos])
                    if test_pos not in group_border_cells:
                        group_border_cells.append(test_pos)
            # Search horizontally
            elif a_cell[1] == int(a_cell[1]):
                # Look for connected half-cell spaces
                for direct in [[0, -1], [0, -1],
                               [-0.5, -0.5], [-0.5, 0.5],
                               [0.5, -0.5], [0.5, 0.5]]:
                    test_pos = [a_cell[0] + direct[0], a_cell[1] + direct[1]]
                    # print('test_pos:', test_pos)
                    # if (test_pos[0] < 0 or test_pos[0]) ...
                    if test_pos in half_cells:
                        # print('foo')
                        if test_pos not in new_group:
                            # print('bar')
                            new_group.append(test_pos)
                            new_group_search.append(test_pos)
                            half_cells.remove(test_pos)
                # Look for connected full-cell spaces
                for direct in [[-0.5, -1], [0.5, -1], [-0.5, 1], [0.5, 1]]:
                    test_pos = [int(round(a_cell[0] + direct[0], 0)),
                                a_cell[1] + direct[1]]
                    index = [i for i, s in enumerate(new_inter_groups)
                             if test_pos in s]
                    full_group = index[0] if index else -1
                    if full_group not in full_groups_attached:
                        full_groups_attached.append(full_group)
                # Look for surrounding border
                for direct in [[-0.5, 0], [0.5, 0]]:
                    test_x, test_y = (int(round(a_cell[0] + direct[0], 0)),
                                      a_cell[1] + direct[1])
                    test_pos = [test_y, test_x, matrix[test_y, test_x]]
                    # print('matrix[*test_pos]:', matrix[*test_pos])
                    if test_pos not in group_border_cells:
                        group_border_cells.append(test_pos)
            else:
                raise ValueError('Something went wrong')

        if not full_groups_attached:
            # print('new_group:', new_group)
            new_group = sorted(new_group, key=lambda x: (x[0], x[1]))
            group_border_cells = sorted(group_border_cells,
                                        key=lambda x: (x[0], x[1]))
            new_inter_groups.append(new_group)
            new_border_cells.append(group_border_cells)
        elif len(full_groups_attached) == 1:  # add halfs to full groups
            # internal space
            new_group = (new_group + 
                         new_inter_groups[full_groups_attached[0]][:]
            new_inter_groups[full_groups_attached[0]] = new_group[:]
            # borders
            group_border_cells = (group_border_cells +
                                  new_border_cells[full_groups_attached[0]])
            group_border_cells = sorted(group_border_cells,
                                        key=lambda x: (x[0], x[1]))
            new_border_cells[full_groups_attached[0]] = group_border_cells[:]
        else:  # add halfs and join connected full groups
            for a_joined_group_no in full_groups_attached:
                # internal space
                new_group = (new_group + new_inter_groups[a_joined_group_no])
                # borders
                group_border_cells = (group_border_cells +
                                      new_border_cells[a_joined_group_no])
            # out with the old
            for index in sorted(full_groups_attached, reverse=True):
                del new_inter_groups[index]
                del new_border_cells[index]
            # in with the new
            new_inter_groups.append(int_temp_group)
            new_border_cells.append(group_border_cells)


    return new_inter_groups, new_border_cells


def crop_shift_cells(border_cells):
    for a_border in border_cells:
        this_border = np.copy(a_border)
        x_coords = np.array([x[0] for x in this_border])
        y_coords = np.array([x[1] for x in this_border])
        x_min = x_coords.min()
        y_min = y_coords.min()
        x_coords = x_coords - x_min
        y_coords = y_coords - y_min
        # y_max = border_y.max()
        border_x = border_x - x_min
        border_y = border_y - y_min
        


def range_of_coords()
    pass


"""
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
"""


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
