# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 10:49:02 2019

@author: PaulJ
"""


import unittest
import collections

import numpy as np

USE_BREAK_DISPLAY = True


def break_evil_pieces(shape):
    if len(shape) == 0:
        return []
    # print('shape:\n', shape)
    # if strings in shape are not equal length, pad
    shape_matrix = shape.strip('\n').split('\n')
    # print('shape_matrix:', shape_matrix)
    line_lens = [len(x) for x in shape_matrix]
    max_len = max(line_lens)
    # print('line_lens:', line_lens, ', max_len:', max_len)
    new_shape = []
    for a_line in shape_matrix:
        new_shape.append(a_line + ''.join(' ' * (max_len - len(a_line))))
    # print('new_shape:\n', new_shape)
    matrix = np.array([[char for char in line]
                       for line in new_shape])
    # print('matrix:\n', matrix)
    # rows, cols = matrix.shape
    # print('rows:', rows, ', cols:', cols)

    inside_full_cells = find_internal_full_cells(matrix)
    # print('inside_full_cells:', inside_full_cells)

    inside_full_groups, border_cells, dead_cells = (
        find_internal_full_groups(matrix, inside_full_cells))
    # print('No full groups:', len(inside_full_groups))
    # print('inside_full_groups:', inside_full_groups)
    # print('border_cells:', border_cells)
    # print('dead_cells:', dead_cells)

    inside_half_cells = find_internal_half_cells(matrix)
    # print('inside_half_cells:', inside_half_cells)

    inside_groups, border_cells = find_internal_half_groups(matrix,
                                                            inside_full_cells,
                                                            inside_half_cells,
                                                            inside_full_groups,
                                                            border_cells,
                                                            dead_cells)
    # print('No groups:', len(inside_groups))
    # print('inside_groups:', inside_groups)
    # print('border_cells:', border_cells)
    # print('half_tunnel_end_groups:', half_tunnel_end_groups)
    # print('dead_cells:', dead_cells)

    inside_groups, border_cells, = crop_shift_cells(inside_groups,
                                                    border_cells)
    # print('border_cells:', border_cells)
    # print('half_tunnel_end_groups:', half_tunnel_end_groups)

    new_matrix_shapes = create_shapes(border_cells)
    # print('new_matrix_shapes:\n', new_matrix_shapes)

    new_matrix_shapes = clean_matrix_shapes(matrix,
                                            new_matrix_shapes)
    # print('\ncleaned new_matrix_shapes:\n', new_matrix_shapes)

    new_matrix_shape_strings = matrices_to_strings(new_matrix_shapes)
    # print('new_matrix_shape_strings:\n', new_matrix_shape_strings)

    # new_matrix_shape_strings = sorted(new_matrix_shape_strings,
    #                                   key=lambda x: len(x))

    return new_matrix_shape_strings


def find_internal_full_cells(matrix):
    # Find all blank spaces. Sort-out which are inside vs. outside in grouping
    # internal_cells = []
    # rows, cols = matrix.shape
    yxs = [list(x) for x in np.where(matrix == ' ')]
    internal_cells = [list(a) for a in zip(yxs[0], yxs[1])]
    return internal_cells


def find_internal_full_groups(matrix, internal_cells):
    rows, cols = matrix.shape
    int_cells = internal_cells[:]
    internal_groups = []
    border_cells = []
    dead_cells = []
    while int_cells:
        a_cell = int_cells.pop(0)
        # print('int_cells:', int_cells)
        new_group = [a_cell]
        new_group_search = [a_cell]
        group_border_cells = []
        dead_group = False
        while new_group_search:
            a_cell = new_group_search.pop(0)
            # Look for connected open space
            for direct in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
                test_pos = [a_cell[0] + direct[0], a_cell[1] + direct[1]]
                test_y, test_x = test_pos
                # print('test_pos:', test_pos)
                if (test_y < 0 or test_y >= rows or
                        test_x < 0 or test_x >= cols):
                    # group is open, disregard
                    dead_group = True
                if test_pos in int_cells:
                    # print('foo')
                    if test_pos not in new_group:
                        # print('bar')
                        new_group.append(test_pos)
                        new_group_search.append(test_pos)
                        int_cells.remove(test_pos)
            # Look for surrounding border
            # print('a_cell:', a_cell)
            for direct in [[-1, 0], [0, 1], [1, 0], [0, -1],
                           [-1, -1], [-1, 1], [1, -1], [1, 1]]:
                test_y, test_x = a_cell[0] + direct[0], a_cell[1] + direct[1]
                # print('test_x:', test_x, ', test_y:', test_y)
                if (test_y < 0 or test_y >= rows or
                        test_x < 0 or test_x >= cols):
                    # group is open, disregard
                    continue
                test_pos = [test_y, test_x, matrix[test_y, test_x]]
                # print('matrix[*test_pos]:', matrix[*test_pos])
                if test_pos[2] in '|-+':
                    if test_pos not in group_border_cells:
                        group_border_cells.append(test_pos)
        if dead_group:
            dead_cells = dead_cells + new_group
            continue
        # print('new_group:', new_group)
        new_group = sorted(new_group, key=lambda x: (x[0], x[1]))
        group_border_cells = sorted(group_border_cells,
                                    key=lambda x: (x[0], x[1]))
        internal_groups.append(new_group)
        border_cells.append(group_border_cells)
    dead_cells = sorted(dead_cells, key=lambda x: (x[0], x[1]))

    return internal_groups, border_cells, dead_cells


def find_internal_half_cells(matrix):
    internal_half_cells = []
    # Search for vertical, narrow passageways
    rows, cols = matrix.shape
    for row_no in range(rows):
        next_row_no = row_no + 1
        for col_no in range(cols):
            next_col_no = col_no + 1
            # Search for vertical, narrow passageways
            # print('row_no:', row_no, ', next_row_no:', next_row_no,
            #       'col_no:', col_no, ', next_col_no:', next_col_no)
            if next_col_no < cols:
                if ((matrix[row_no, col_no] in ('|', '+') and
                     matrix[row_no, next_col_no] == '|') or
                    (matrix[row_no, next_col_no] in ('|', '+') and
                     matrix[row_no, col_no] == '|')):
                    internal_half_cells.append([row_no, col_no + 0.5])
            # Search for horiz, narrow passageways
            if next_row_no < rows:
                if ((matrix[row_no, col_no] in ('-', '+') and
                     matrix[next_row_no, col_no] == '-') or
                    (matrix[next_row_no, col_no] in ('-', '+') and
                     matrix[row_no, col_no] == '-')):
                    internal_half_cells.append([row_no + 0.5, col_no])
                # Search for single half-cell box ++\n++, i.e. eggs
                if next_col_no < cols:
                    if (matrix[row_no, col_no] == '+' and
                        matrix[row_no, next_col_no] == '+' and
                        matrix[next_row_no, col_no] == '+' and
                            matrix[next_row_no, next_col_no] == '+'):
                        internal_half_cells.append([row_no + 0.5,
                                                    col_no + 0.5])
    internal_half_cells = sorted(internal_half_cells,
                                 key=lambda x: (x[0], x[1]))
    return internal_half_cells


def find_internal_half_groups(matrix,
                              full_cells,
                              int_half_cells,
                              in_full_groups,
                              border_cells,
                              dead_cells):
    rows, cols = matrix.shape
    half_cells = int_half_cells[:]
    # internal_groups = []
    new_inter_groups = in_full_groups[:]
    new_border_cells = border_cells[:]
    while half_cells:
        a_cell = half_cells.pop(0)
        # print('int_cells:', int_cells)
        new_group = [a_cell]
        full_groups_attached = []
        new_group_search = [a_cell]
        group_border_cells = []
        dead_group = False
        while new_group_search:
            a_cell = new_group_search.pop(0)
            # print('Searching from a_cell:', a_cell)
            # print('Remaining new_group_search:', new_group_search)
            # Check for single quarter cell first
            if (a_cell[0] != int(a_cell[0])) and (a_cell[1] != int(a_cell[1])):
                # print('a_cell:', a_cell, ', searching for egg')
                for direct in [[-0.5, -0.5], [-0.5, 0.5],
                               [0.5, -0.5], [0.5, 0.5]]:
                    test_y, test_x = (int(round(a_cell[0] + direct[0], 0)),
                                      int(round(a_cell[1] + direct[1], 0)))
                    test_cell = [test_y, test_x, matrix[test_y, test_x]]
                    group_border_cells.append(test_cell)
            elif a_cell[0] == int(a_cell[0]):
                # Search vertically
                # print('a_cell:', a_cell, ', searching vertically')
                # Look for connected half-cell spaces
                for direct in [[-1, 0], [1, 0],
                               [-0.5, -0.5], [-0.5, 0.5],
                               [0.5, -0.5], [0.5, 0.5]]:
                    test_pos = [round(a_cell[0] + direct[0], 1),
                                round(a_cell[1] + direct[1], 1)]
                    if test_pos[0] < 0 or test_pos[0] >= rows:
                        dead_group = True
                        continue
                    if test_pos in dead_cells:
                        dead_group = True
                        continue
                    # print('vetical half-cell search: test_pos:', test_pos)
                    # if (test_pos[0] < 0 or test_pos[0]) ...
                    if test_pos in half_cells:
                        # print('foo')
                        if test_pos not in new_group:
                            # print('bar')
                            new_group.append(test_pos)
                            new_group_search.append(test_pos)
                            half_cells.remove(test_pos)
                    # print('new_group_search:', new_group_search)
                # Look for connected full-cell spaces
                for direct in [[-1, -0.5], [-1, 0.5], [1, -0.5], [1, 0.5]]:
                    test_pos = [int(round(a_cell[0] + direct[0], 0)),
                                int(round(a_cell[1] + direct[1], 0))]
                    if test_pos[0] < 0 or test_pos[0] >= rows:
                        dead_group = True
                        continue
                    if test_pos in dead_cells:
                        dead_group = True
                        continue
                    index = [i for i, s in enumerate(new_inter_groups)
                             if test_pos in s]
                    full_group = index[0] if index else -1
                    if (full_group != -1 and
                            full_group not in full_groups_attached):
                        full_groups_attached.append(full_group)
                # Look for surrounding border
                for direct in [[0, -0.5], [0, 0.5], [-1, -0.5], [-1, 0.5],
                               [1, -0.5], [1, 0.5]]:
                    test_pos = [int(round(a_cell[0] + direct[0], 0)),
                                int(round(a_cell[1] + direct[1], 0))]
                    # print('test_pos:', test_pos)
                    test_y, test_x = test_pos
                    test_cell = [test_y, test_x, matrix[test_y, test_x]]
                    # print('matrix[*test_pos]:', matrix[*test_pos])
                    # print('current group_border_cells:', group_border_cells)
                    if test_cell not in group_border_cells:
                        # print('adding border:', test_cell)
                        group_border_cells.append(test_cell)
            elif a_cell[1] == int(a_cell[1]):
                # Search horizontally
                # print('a_cell:', a_cell, ', searching horizontally')
                # Look for connected half-cell spaces
                for direct in [[0, -1], [0, 1],
                               [-0.5, -0.5], [-0.5, 0.5],
                               [0.5, -0.5], [0.5, 0.5]]:
                    test_pos = [round(a_cell[0] + direct[0], 1),
                                round(a_cell[1] + direct[1], 1)]
                    # print('test_pos:', test_pos)
                    if test_pos[1] < 0 or test_pos[1] >= cols:
                        dead_group = True
                        continue
                    if test_pos in dead_cells:
                        dead_group = True
                        continue
                    # if (test_pos[0] < 0 or test_pos[0]) ...
                    if test_pos in half_cells:
                        # print('foo')
                        if test_pos not in new_group:
                            # print('bar')
                            new_group.append(test_pos)
                            new_group_search.append(test_pos)
                            half_cells.remove(test_pos)
                # Look for connected full-cell spaces
                # print('Look for connected full-cell spaces')
                for direct in [[-0.5, -1], [0.5, -1], [-0.5, 1], [0.5, 1]]:
                    test_pos = [int(round(a_cell[0] + direct[0], 0)),
                                int(round(a_cell[1] + direct[1], 0))]
                    # print('test_pos:', test_pos)
                    if test_pos[1] < 0 or test_pos[1] >= cols:
                        dead_group = True
                        continue
                    if test_pos in dead_cells:
                        dead_group = True
                        continue
                    index = [i for i, s in enumerate(new_inter_groups)
                             if test_pos in s]
                    # print('index:', index)
                    full_group = index[0] if index else -1
                    if (full_group != -1 and
                            full_group not in full_groups_attached):
                        full_groups_attached.append(full_group)
                    # print('full_groups_attached:', full_groups_attached)
                # print('new_group:', new_group)
                # Look for surrounding border
                for direct in [[-0.5, 0], [0.5, 0], [-0.5, -1], [-0.5, 1],
                               [0.5, -1], [0.5, 1]]:
                    # print('a_cell:', a_cell)
                    test_pos = [int(round(a_cell[0] + direct[0], 0)),
                                int(round(a_cell[1] + direct[1], 0))]
                    test_y, test_x = test_pos
                    # print('test_y:', test_y, ', test_x:', test_x)
                    test_cell = [test_y, test_x, matrix[test_y, test_x]]
                    # print('matrix[*test_pos]:', matrix[*test_pos])
                    if test_cell not in group_border_cells:
                        group_border_cells.append(test_cell)
            else:
                raise ValueError('Something went wrong')

        # print('372:new_group:', new_group)
        # print('373:full_gropus_attached:', full_groups_attached)
        # print('374:dead_group:', dead_group)

        if not full_groups_attached:
            # print('new_group:', new_group)
            new_group = sorted(new_group, key=lambda x: (x[0], x[1]))
            if dead_group:
                dead_cells = dead_cells + new_group
                continue
            group_border_cells = sorted(group_border_cells,
                                        key=lambda x: (x[0], x[1]))
            new_inter_groups.append(new_group)
            new_border_cells.append(group_border_cells)
        elif len(full_groups_attached) == 1:  # add halfs to full groups
            # internal space
            new_group = (new_group +
                         new_inter_groups[full_groups_attached[0]][:])
            # print('new_group:', new_group)
            if dead_group:
                dead_cells = dead_cells + new_group
                # print('dead_cells:', dead_cells)
                del new_inter_groups[full_groups_attached[0]]
                del new_border_cells[full_groups_attached[0]]
                # print('new_inter_groups:', new_inter_groups)
                continue
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
            # print('new_group:', new_group)

            # out with the old
            for index in sorted(full_groups_attached, reverse=True):
                del new_inter_groups[index]
                del new_border_cells[index]

            # in with the new
            if dead_group:
                dead_cells = dead_cells + new_group
                continue
            new_inter_groups.append(new_group)
            new_border_cells.append(group_border_cells)
        # print('end of groups:new_inter_groups:', new_inter_groups)
        # print('end of groups:new_border_cells:', new_border_cells)

    return new_inter_groups, new_border_cells


def crop_shift_cells(inside_groups, border_cells):
    new_inside_groups = []
    new_border_cells = []
    for shape_no, a_border in enumerate(border_cells):
        # print('a_border:', a_border)
        this_group = np.copy(inside_groups[shape_no])
        this_border = np.copy(a_border)
        # print('this_border:', this_border)
        gr_y_coords = np.array([int(border[0]) for border in this_group])
        gr_x_coords = np.array([int(border[1]) for border in this_group])
        y_coords = np.array([int(border[0]) for border in this_border])
        x_coords = np.array([int(border[1]) for border in this_border])
        shape = np.array([border[2] for border in this_border])
        # print('y_coords:', y_coords, ', x_coords:', x_coords)
        # print('ht_eg_y_coords:', ht_eg_y_coords, ', ht_eg_x_coords:',
        #       ht_eg_x_coords)
        y_min = y_coords.min()
        x_min = x_coords.min()
        gr_y_coords = gr_y_coords - y_min
        gr_x_coords = gr_x_coords - x_min
        y_coords = y_coords - y_min
        x_coords = x_coords - x_min
        # y_max = border_y.max()
        group = list(zip(gr_y_coords, gr_x_coords))
        border = list(zip(y_coords, x_coords, shape))
        new_inside_groups.append(group)
        new_border_cells.append(border)
    return new_inside_groups, new_border_cells


def create_shapes(border_cells):
    new_matrix_group = []
    new_matrix_str_group = []
    for a_border_group in border_cells:
        y_coords = np.array([int(border[0]) for border in a_border_group])
        x_coords = np.array([int(border[1]) for border in a_border_group])
        shape = np.array([border[2] for border in a_border_group])
        # print('y_coords:', y_coords, ', x_coords:', x_coords)
        rows = y_coords.max() + 1
        cols = x_coords.max() + 1
        # new_matrix = np.array(rows, cols)
        new_matrix = np.full((rows, cols), ' ')
        for a_border_no in range(len(y_coords)):
            new_matrix[y_coords[a_border_no], x_coords[a_border_no]] = (
                shape[a_border_no])
        new_matrix_str = '\n'.join([''.join(item for item in row)
                                   for row in new_matrix])
        new_matrix_group.append(new_matrix)
        new_matrix_str_group.append(new_matrix_str)
    # return new_matrix_str_group
    return new_matrix_group


def clean_matrix_shapes(matrix, matrix_shapes):
    rows, cols = matrix.shape
    cleaned_matrix_shapes = []
    for shape_no, a_matrix_shape in enumerate(matrix_shapes):
        rows, cols = a_matrix_shape.shape
        intersections = list(zip(*[list(x)
                                   for x in np.where(a_matrix_shape == '+')]))
        # print('intersections:', intersections)
        for intersect in intersections:
            # intersect = list(intersect)
            y_coord, x_coord = intersect
            x_pre = x_coord - 1
            x_post = x_coord + 1
            y_pre = y_coord - 1
            y_post = y_coord + 1
            # print('intersect:', intersect)
            # print('list(intersect):', list(intersect))
            # print('half_tunnel_end_groups[shape_no]:',
            #       half_tunnel_end_groups[shape_no])
            north = a_matrix_shape[y_pre, x_coord] if y_pre >= 0 else ''
            south = a_matrix_shape[y_post, x_coord] if y_post < rows else ''
            east = a_matrix_shape[y_coord, x_post] if x_post < cols else ''
            west = a_matrix_shape[y_coord, x_pre] if x_pre >= 0 else ''
            horiz_sym = ('-', '+')
            vert_sym = ('|', '+')
            if not ((west in horiz_sym or east in horiz_sym) and
                    (north in vert_sym or south in vert_sym)):
                if (west in horiz_sym and east in horiz_sym):
                    print('replacing at intersect:', intersect, ', -')
                    a_matrix_shape[intersect] = '-'
                elif (north in vert_sym and south in vert_sym):
                    print('replacing at intersect:', intersect, ', |')
                    a_matrix_shape[intersect] = '|'
                else:
                    raise ValueError("I'm confused")

        cleaned_matrix_shapes.append(a_matrix_shape)
    return cleaned_matrix_shapes


def matrices_to_strings(matrix_shapes):
    new_matrix_str_group = []
    for a_matrix_shape in matrix_shapes:
        matrix_str = [''.join(item for item in row)
                      for row in a_matrix_shape]
        matrix_str = [x.rstrip() for x in matrix_str]
        new_matrix_str = '\n'.join(matrix_str)
        new_matrix_str_group.append(new_matrix_str)
    return new_matrix_str_group


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
        answer = ["""
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
        print('result:\n')
        for a_result in result:
            print(a_result)
        print('answer:\n')
        for an_answer in answer:
            print(an_answer)
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
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
""".strip('\n'), ]
        result = break_evil_pieces(shape)
        print('result:\n')
        for a_result in result:
            print(a_result)
        print('answer:\n')
        for an_answer in answer:
            print(an_answer)
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
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
""".strip('\n'), ]
        result = break_evil_pieces(shape)
        print('result:\n')
        for a_result in result:
            print(a_result)
        print('answer:\n')
        for an_answer in answer:
            print(an_answer)
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
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
        print('shape:\n', shape)
        print('result:\n')
        for a_result in result:
            print(a_result)
        print('answer:\n')
        for an_answer in answer:
            print(an_answer)
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
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
        print('result:\n')
        for a_result in result:
            print(a_result)
        print('answer:\n')
        for an_answer in answer:
            print(an_answer)
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
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
""".strip('\n'), ]
        result = break_evil_pieces(shape)
        print('result:\n')
        for a_result in result:
            print(a_result)
        print('answer:\n')
        for an_answer in answer:
            print(an_answer)
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
        print('correct!')

        # Test 7 - Don't forget the eggs! (you'll understand later...)
        print('Test 7: ', end='')
        shape = """
++
++
""".strip('\n')
        answer = [shape]
        result = break_evil_pieces(shape)
        print('result:\n')
        for a_result in result:
            print(a_result)
        print('answer:\n')
        for an_answer in answer:
            print(an_answer)
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
        print('correct!')

        # Test 8 - Train?
        print('Test 8: ', end='')
        shape = """
+----++----++----++----+
+----++----++----++----+
""".strip('\n')
        answer = ["""
++
++
""".strip('\n'),
"""
++
++
""".strip('\n'),
"""
++
++
""".strip('\n'),
"""
+----+
+----+
""".strip('\n'),
"""
+----+
+----+
""".strip('\n'),
"""
+----+
+----+
""".strip('\n'),
"""
+----+
+----+
""".strip('\n')]
        result = break_evil_pieces(shape)
        # print('result:\n')
        for a_result in result:
            pass
            # print(a_result, '\n\n')
        # print('answer:\n')
        for an_answer in answer:
            pass
            # print(an_answer, '\n\n')
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
        print('correct!')

        # Test - 9 - Yin-Yang
        print('Test 9: ', end='')
        shape = """
+-------------------++--+
|                   ||  |
|                   ||  |
|  +----------------+|  |
|  |+----------------+  |
|  ||                   |
+--++-------------------+
""".strip('\n')
        answer = ["""
+-------------------+
|                   |
|                   |
|  +----------------+
|  |
|  |
+--+
""".strip('\n'),
"""
                 ++
                 ||
                 ||
+----------------+|
|+----------------+
||
++
""".strip('\n'),
"""
                 +--+
                 |  |
                 |  |
                 |  |
+----------------+  |
|                   |
+-------------------+
""".strip('\n')]
        result = break_evil_pieces(shape)
        print('result:\n')
        for a_result in result:
            print(a_result, '\n\n')
        print('answer:\n')
        for an_answer in answer:
            print(an_answer, '\n\n')
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
        print('correct!')

        # Test - 10 - Blank
        print('Test 10: ', end='')
        shape = """
""".strip('\n')
        answer = []
        result = break_evil_pieces(shape)
        print('result:\n')
        for a_result in result:
            print(a_result, '\n\n')
        print('answer:\n')
        for an_answer in answer:
            print(an_answer, '\n\n')
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
        print('correct!')

        # Test - 11 - Vortex
        print('Test 11: ', end='')
        shape = """
+-----+
+----+|
|+--+||
||++|||
||++|||
||+-+||
|+---+|
+-----+
""".strip('\n')
        answer = ["""
++
++
""".strip('\n'),
"""
+-----+
+----+|
|+--+||
||++|||
||++|||
||+-+||
|+---+|
+-----+
""".strip('\n')]
        print('shape:\n', shape)
        result = break_evil_pieces(shape)
        print('result:\n')
        for a_result in result:
            print(a_result, '\n\n')
        print('answer:\n')
        for an_answer in answer:
            print(an_answer, '\n\n')
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
        print('correct!')

        # Test - 12 - Vortex 2
        print('Test 12: ', end='')
        shape = """
          
 +-----+ 
 +----+| 
 |+--+|| 
 ||++||| 
 ||++||| 
 ||+-+|| 
 |+---+| 
 +-----+ 
""".strip('\n')
        answer = ["""
++
++
""".strip('\n'),
"""
+-----+
+----+|
|+--+||
||++|||
||++|||
||+-+||
|+---+|
+-----+
""".strip('\n')]
        print('shape:\n', shape)
        result = break_evil_pieces(shape)
        print('result:\n')
        for a_result in result:
            print(a_result, '\n\n')
        print('answer:\n')
        for an_answer in answer:
            print(an_answer, '\n\n')
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
        print('correct!')


        # Test - 13 - 
        print('Test 13: ', end='')
        shape = """
+-----------------+
|+---------------+|
||        ++     ||
|+--------+|     ||
+----------+     ||
                 ||
+----------------+|
|+----------------+
||
|+------+
+-------+
""".strip('\n')
        answer = [shape]
        print('shape:\n', shape)
        result = break_evil_pieces(shape)
        print('result:\n')
        for a_result in result:
            print(a_result, '\n\n')
        print('answer:\n')
        for an_answer in answer:
            print(an_answer, '\n\n')
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
        print('correct!')

        # Test - 14 - 
        print('Test 14: ', end='')
        shape = """
+-----------------+
|+---------------+|
||        ++     ||
|+--------+|     ||
+----------+     ||
+----------------+|
|+----------------+
||
|+------+
+-------+
""".strip('\n')
        answer = [
"""
 +---------------+
 |        ++     |
 +--------+|     |
+----------+     |
+----------------+
""".strip('\n'),
"""
+-----------------+
|+---------------+|
||        ++     ||
|+--------+|     ||
+----------+     ||
+----------------+|
|+----------------+
||
|+------+
+-------+
""".strip('\n')]
        print('shape:\n', shape)
        result = break_evil_pieces(shape)
        print('result:\n')
        for a_result in result:
            print(a_result, '\n\n')
        print('answer:\n')
        for an_answer in answer:
            print(an_answer, '\n\n')
        pass_result = (collections.Counter(result) ==
                       collections.Counter(answer))
        self.assertTrue(pass_result)
        print('correct!')


if __name__ == '__main__':
    unittest.main()

"""
Result:

"""
