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
    # print('\nshape:\n', shape)
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

    inside_full_groups, border_cells, outside_space, corner_keeper_groups = (
        find_internal_full_groups(matrix, inside_full_cells))
    # print('No full groups:', len(inside_full_groups))
    # print('inside_full_groups:', inside_full_groups)
    # print('border_cells:', border_cells)
    # print('outside_space:', outside_space)
    # print('corner_keeper_groups:', corner_keeper_groups)

    inside_half_cells = find_internal_half_cells(matrix)
    print('inside_half_cells:', inside_half_cells)

    inside_groups, border_cells, corner_keeper_groups, outside_space = (
        find_internal_half_groups(matrix,
                                  inside_full_cells,
                                  inside_half_cells,
                                  inside_full_groups,
                                  border_cells,
                                  outside_space,
                                  corner_keeper_groups))
    # print('No groups:', len(inside_groups))
    # print('inside_groups:', inside_groups)
    # print('border_cells:', border_cells)
    # print('corner_keeper_groups:', corner_keeper_groups)
    # print('outside_space:', outside_space)

    inside_groups, border_cells, corner_keeper_groups, outside_space = (
        crop_shift_cells(inside_groups,
                         border_cells,
                         corner_keeper_groups,
                         outside_space))
    # print('inside_groups:', inside_groups)
    # print('border_cells:', border_cells)
    # print('corner_keeper_groups:', corner_keeper_groups)
    # print('outside_space[0]:', outside_space[0])

    new_matrix_shapes = create_shapes(border_cells)
    # print('new_matrix_shapes:\n', new_matrix_shapes)

    new_matrix_shapes = clean_matrix_shapes(matrix,
                                            new_matrix_shapes,
                                            inside_groups,
                                            corner_keeper_groups,
                                            outside_space)
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
    internal_cells = {tuple(a) for a in zip(yxs[0], yxs[1])}
    return internal_cells


def find_internal_full_groups(matrix, internal_cells):
    rows, cols = matrix.shape
    int_cells = internal_cells.copy()
    internal_groups = []
    border_cells = []
    corner_keeper_groups = []
    outside_space = set()
    edges = ('|', '-', '+')
    while int_cells:
        a_cell = int_cells.pop()
        # print('int_cells:', int_cells)
        new_group = {a_cell}
        new_group_search = {a_cell}
        group_border_cells = set()
        corner_keepers = set()
        dead_group = False
        while new_group_search:
            a_cell = new_group_search.pop()
            # Look for connected open space
            for direct in [[-1, 0], [0, 1], [1, 0], [0, -1],
                           [-1, -1], [-1, 1], [1, -1], [1, 1]]:
                test_pos = (a_cell[0] + direct[0], a_cell[1] + direct[1])
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
                        new_group.add(test_pos)
                        new_group_search.add(test_pos)
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
                test_pos = (test_y, test_x, matrix[test_y, test_x])
                # print('matrix[*test_pos]:', matrix[*test_pos])
                if test_pos[2] in '|-+':
                    # if test_pos not in group_border_cells:
                    group_border_cells.add(test_pos)
            # Look for corners to keep intersection character
            for direct in [[[-1, -1], [0, -1], [-1, 0]],
                           [[-1, 1], [-1, 0], [0, 1]],
                           [[1, 1], [0, 1], [1, 0]],
                           [[1, -1], [1, 0], [0, -1]]]:
                corn_y = a_cell[0] + direct[0][0]
                if corn_y < 0 or corn_y >= rows:
                    continue
                corn_x = a_cell[1] + direct[0][1]
                if corn_x < 0 or corn_x >= cols:
                    continue
                if matrix[corn_y, corn_x] != '+':
                    continue
                edge_1_y = a_cell[0] + direct[1][0]
                edge_1_x = a_cell[1] + direct[1][1]
                edge_2_y = a_cell[0] + direct[2][0]
                edge_2_x = a_cell[1] + direct[2][1]
                if (matrix[edge_1_y, edge_1_x] in edges and
                        matrix[edge_2_y, edge_2_x] in edges):
                    # if [corn_y, corn_x] not in corner_keepers:
                    corner_keepers.add((corn_y, corn_x))

        if dead_group:
            outside_space = outside_space | new_group  # | == union
            continue
        # print('new_group:', new_group)
        # new_group = sorted(new_group, key=lambda x: (x[0], x[1]))
        # group_border_cells = sorted(group_border_cells,
        #                            key=lambda x: (x[0], x[1]))
        # corner_keeper_group = sorted(corner_keeper_group, key=lambda x:
        # (x[0], x[1]))
        internal_groups.append(new_group)
        border_cells.append(group_border_cells)
        corner_keeper_groups.append(corner_keepers)
    # outside_space = sorted(outside_space, key=lambda x: (x[0], x[1]))

    return internal_groups, border_cells, outside_space, corner_keeper_groups


def find_internal_half_cells(matrix):
    internal_half_cells = set()
    # Search for vertical, narrow passageways
    rows, cols = matrix.shape
    for row_no in range(rows):
        next_row_no = row_no + 1
        for col_no in range(cols):
            next_col_no = col_no + 1
            # Search for vertical, narrow passageways
            print('row_no:', row_no, ', next_row_no:', next_row_no,
                  'col_no:', col_no, ', next_col_no:', next_col_no)
            if next_col_no < cols:
                if ((matrix[row_no, col_no] in ('|', '+') and
                     matrix[row_no, next_col_no] == '|') or
                    (matrix[row_no, next_col_no] in ('|', '+') and
                     matrix[row_no, col_no] == '|')):
                    internal_half_cells.add((row_no, col_no + 0.5))
            # Search for horiz, narrow passageways
            if next_row_no < rows:
                if ((matrix[row_no, col_no] in ('-', '+') and
                     matrix[next_row_no, col_no] == '-') or
                    (matrix[next_row_no, col_no] in ('-', '+') and
                     matrix[row_no, col_no] == '-')):
                    internal_half_cells.add((row_no + 0.5, col_no))
                # Search for single half-cell box ++\n++, i.e. eggs
                if next_col_no < cols:
                    if (matrix[row_no, col_no] == '+' and
                        matrix[row_no, next_col_no] == '+' and
                        matrix[next_row_no, col_no] == '+' and
                            matrix[next_row_no, next_col_no] == '+'):
                        internal_half_cells.add((row_no + 0.5, col_no + 0.5))
    # internal_half_cells = sorted(internal_half_cells,
    #                              key=lambda x: (x[0], x[1]))
    return internal_half_cells


def find_internal_half_groups(matrix,
                              full_cells,
                              int_half_cells,
                              in_full_groups,
                              border_cells,
                              outside_space,
                              corner_keeper_groups):
    rows, cols = matrix.shape
    half_cells = int_half_cells.copy()
    # internal_groups = []
    internal_groups = in_full_groups[:]
    new_border_cells = border_cells[:]
    new_corner_keeper_groups = corner_keeper_groups[:]
    while half_cells:
        a_cell = half_cells.pop()
        # print('int_cells:', int_cells)
        new_group = {a_cell}
        full_groups_attached = []
        new_group_search = [a_cell]
        group_border_cells = set()
        half_tunnel_ends = set()
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
                    test_cell = (test_y, test_x, matrix[test_y, test_x])
                    group_border_cells.add(test_cell)
            elif a_cell[0] == int(a_cell[0]):
                # Search vertically
                # print('a_cell:', a_cell, ', searching vertically')
                # Look for connected half-cell spaces
                for direct in [[-1, 0], [1, 0],
                               [-0.5, -0.5], [-0.5, 0.5],
                               [0.5, -0.5], [0.5, 0.5]]:
                    test_pos = (round(a_cell[0] + direct[0], 1),
                                round(a_cell[1] + direct[1], 1))
                    if test_pos[0] < 0 or test_pos[0] >= rows:
                        dead_group = True
                        continue
                    if test_pos in outside_space:
                        dead_group = True
                        continue
                    # print('vetical half-cell search: test_pos:', test_pos)
                    # if (test_pos[0] < 0 or test_pos[0]) ...
                    if test_pos in half_cells:
                        # print('foo')
                        if test_pos not in new_group:
                            # print('bar')
                            new_group.add(test_pos)
                            new_group_search.append(test_pos)
                            half_cells.remove(test_pos)
                    # print('new_group_search:', new_group_search)
                # Look for connected full-cell spaces
                for direct in [[-1, -0.5], [-1, 0.5], [1, -0.5], [1, 0.5]]:
                    test_pos = (int(round(a_cell[0] + direct[0], 0)),
                                int(round(a_cell[1] + direct[1], 0)))
                    if test_pos[0] < 0 or test_pos[0] >= rows:
                        dead_group = True
                        continue
                    if test_pos in outside_space:
                        dead_group = True
                        continue
                    # print('internal_groups:', internal_groups)
                    # print('test_pos:', test_pos)
                    index = [i for i, s in enumerate(internal_groups)
                             if test_pos in s]
                    # print('index:', index)
                    full_group = index[0] if index else -1
                    if (full_group != -1 and
                            full_group not in full_groups_attached):
                        full_groups_attached.append(full_group)
                # Look for surrounding border
                for direct in [[0, -0.5], [0, 0.5], [-1, -0.5], [-1, 0.5],
                               [1, -0.5], [1, 0.5]]:
                    test_pos = (int(round(a_cell[0] + direct[0], 0)),
                                int(round(a_cell[1] + direct[1], 0)))
                    # print('test_pos:', test_pos)
                    test_y, test_x = test_pos
                    test_cell = (test_y, test_x, matrix[test_y, test_x])
                    # print('matrix[*test_pos]:', matrix[*test_pos])
                    # print('current group_border_cells:', group_border_cells)
                    # if test_cell not in group_border_cells:
                    # print('adding border:', test_cell)
                    group_border_cells.add(test_cell)
                # Look for terminating half-cell tunnels to preserve ends
                for direct_pair in [[[-1, -0.5], [-1, 0.5]],
                                    [[1, -0.5], [1, 0.5]]]:
                    test_1 = (int(round(a_cell[0] + direct_pair[0][0], 0)),
                              int(round(a_cell[1] + direct_pair[0][1], 0)))
                    test_2 = (int(round(a_cell[0] + direct_pair[1][0], 0)),
                              int(round(a_cell[1] + direct_pair[1][1], 0)))
                    test_1_y, test_1_x = test_1
                    test_2_y, test_2_x = test_2
                    if (matrix[test_1_y, test_1_x] == '+' and
                            matrix[test_2_y, test_2_x] == '+'):
                        half_tunnel_ends.add(test_1)
                        half_tunnel_ends.add(test_2)
            elif a_cell[1] == int(a_cell[1]):
                # Search horizontally
                # print('a_cell:', a_cell, ', searching horizontally')
                # Look for connected half-cell spaces
                for direct in [[0, -1], [0, 1],
                               [-0.5, -0.5], [-0.5, 0.5],
                               [0.5, -0.5], [0.5, 0.5]]:
                    test_pos = (round(a_cell[0] + direct[0], 1),
                                round(a_cell[1] + direct[1], 1))
                    # print('test_pos:', test_pos)
                    if test_pos[1] < 0 or test_pos[1] >= cols:
                        dead_group = True
                        continue
                    if test_pos in outside_space:
                        dead_group = True
                        continue
                    # if (test_pos[0] < 0 or test_pos[0]) ...
                    if test_pos in half_cells:
                        # print('foo')
                        if test_pos not in new_group:
                            # print('bar')
                            new_group.add(test_pos)
                            new_group_search.append(test_pos)
                            half_cells.remove(test_pos)
                # Look for connected full-cell spaces
                # print('Look for connected full-cell spaces')
                for direct in [[-0.5, -1], [0.5, -1], [-0.5, 1], [0.5, 1]]:
                    test_pos = (int(round(a_cell[0] + direct[0], 0)),
                                int(round(a_cell[1] + direct[1], 0)))
                    # print('test_pos:', test_pos)
                    if test_pos[1] < 0 or test_pos[1] >= cols:
                        dead_group = True
                        continue
                    if test_pos in outside_space:
                        dead_group = True
                        continue
                    index = [i for i, s in enumerate(internal_groups)
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
                    test_pos = (int(round(a_cell[0] + direct[0], 0)),
                                int(round(a_cell[1] + direct[1], 0)))
                    test_y, test_x = test_pos
                    # print('test_y:', test_y, ', test_x:', test_x)
                    test_cell = (test_y, test_x, matrix[test_y, test_x])
                    # print('matrix[*test_pos]:', matrix[*test_pos])
                    # if test_cell not in group_border_cells:
                    group_border_cells.add(test_cell)
                # Look for terminating half-cell tunnels to preserve ends
                for direct_pair in [[[-0.5, -1], [0.5, -1]],
                                    [[-0.5, 1], [0.5, 1]]]:
                    test_1 = (int(round(a_cell[0] + direct_pair[0][0], 0)),
                              int(round(a_cell[1] + direct_pair[0][1], 0)))
                    test_2 = (int(round(a_cell[0] + direct_pair[1][0], 0)),
                              int(round(a_cell[1] + direct_pair[1][1], 0)))
                    test_1_y, test_1_x = test_1
                    test_2_y, test_2_x = test_2
                    if (matrix[test_1_y, test_1_x] == '+' and
                            matrix[test_2_y, test_2_x] == '+'):
                        half_tunnel_ends.add(test_1)
                        half_tunnel_ends.add(test_2)
            else:
                raise ValueError('Something went wrong')

        # print('372:new_group:', new_group)
        # print('373:full_gropus_attached:', full_groups_attached)
        # print('374:dead_group:', dead_group)

        if not full_groups_attached:
            # print('new_group:', new_group)
            # new_group = sorted(new_group, key=lambda x: (x[0], x[1]))
            if dead_group:
                outside_space = outside_space | new_group
                continue
            # group_border_cells = sorted(group_border_cells,
            #                             key=lambda x: (x[0], x[1]))
            internal_groups.append(new_group)
            new_border_cells.append(group_border_cells)
            new_corner_keeper_groups.append(half_tunnel_ends)
        elif len(full_groups_attached) == 1:  # add halfs to full groups
            # internal space
            new_group = (new_group |
                         internal_groups[full_groups_attached[0]])
            # print('new_group:', new_group)
            if dead_group:
                outside_space = outside_space | new_group
                # print('outside_space:', outside_space)
                del internal_groups[full_groups_attached[0]]
                del new_border_cells[full_groups_attached[0]]
                del new_corner_keeper_groups[full_groups_attached[0]]
                # print('internal_groups:', internal_groups)
                continue
            internal_groups[full_groups_attached[0]] = new_group.copy()
            # borders
            group_border_cells = (group_border_cells |
                                  new_border_cells[full_groups_attached[0]])
            # group_border_cells = sorted(group_border_cells,
            #                             key=lambda x: (x[0], x[1]))
            new_border_cells[full_groups_attached[0]] = (
                group_border_cells.copy())
            new_corner_keeper_groups[full_groups_attached[0]] = (
                half_tunnel_ends.copy())
        else:  # add halfs and join connected full groups
            for a_joined_group_no in full_groups_attached:
                # internal space
                new_group = (new_group | internal_groups[a_joined_group_no])
                # borders
                group_border_cells = (group_border_cells |
                                      new_border_cells[a_joined_group_no])
                half_tunnel_ends = (
                    half_tunnel_ends |
                    new_corner_keeper_groups[a_joined_group_no])
            # print('new_group:', new_group)

            # out with the old
            for index in sorted(full_groups_attached, reverse=True):
                del internal_groups[index]
                del new_border_cells[index]
                del new_corner_keeper_groups[index]

            # in with the new
            if dead_group:
                outside_space = outside_space | new_group
                continue
            internal_groups.append(new_group)
            new_border_cells.append(group_border_cells)
            new_corner_keeper_groups.append(half_tunnel_ends)
        # print('end of groups:internal_groups:', internal_groups)
        # print('end of groups:new_border_cells:', new_border_cells)

    return (internal_groups, new_border_cells, new_corner_keeper_groups,
            outside_space)


def crop_shift_cells(inside_groups, border_cells, corner_keeper_groups,
                     outside_space):
    new_inside_groups = []
    new_border_groups = []
    new_border_coords_groups = []
    new_corner_keeper_groups = []
    new_outside_space_groups = []  # Outside space becomes list for each group
    all_space_groups = []  # for each shape, a set of all space in its coords
    all_space_global = outside_space.copy()
    for shape_no, _ in enumerate(inside_groups):
        all_space_global = (all_space_global | inside_groups[shape_no] |
                            border_cells[shape_no])
    for shape_no, a_border in enumerate(border_cells):
        # print('a_border:', a_border)
        # print('a_border:', a_border)
        # Convert Border
        y_coords = np.array([int(border[0]) for border in a_border])
        x_coords = np.array([int(border[1]) for border in a_border])
        shape = np.array([border[2] for border in a_border])
        y_min = y_coords.min()
        x_min = x_coords.min()
        y_coords = y_coords - y_min
        x_coords = x_coords - x_min
        border = set(zip(y_coords, x_coords, shape))
        border_coords = set(zip(y_coords, x_coords))
        new_border_groups.append(border)
        new_border_coords_groups.append(border_coords)

        # Convert Inside Space for group
        gr_y_coords = np.array(
            [a_space[0] for a_space in inside_groups[shape_no]])
        gr_x_coords = np.array(
            [a_space[1] for a_space in inside_groups[shape_no]])
        gr_y_coords = gr_y_coords - y_min
        gr_x_coords = gr_x_coords - x_min
        group = set(zip(gr_y_coords, gr_x_coords))
        new_inside_groups.append(group)

        # Convert corner keeper group
        ht_eg_y_coords = np.array(
            [int(eg[0]) for eg in corner_keeper_groups[shape_no]])
        ht_eg_x_coords = np.array(
            [int(eg[1]) for eg in corner_keeper_groups[shape_no]])
        ht_eg_y_coords = ht_eg_y_coords - y_min
        ht_eg_x_coords = ht_eg_x_coords - x_min
        ht_eg = set(zip(ht_eg_y_coords, ht_eg_x_coords))
        new_corner_keeper_groups.append(ht_eg)

        # Convert all space to local (to shape) array
        all_space_y = np.array([a_space[0] for a_space in all_space_global])
        all_space_x = np.array([a_space[1] for a_space in all_space_global])
        all_space_y = all_space_y - y_min
        all_space_x = all_space_x - x_min
        all_space = set(zip(all_space_y, all_space_x))
        all_space_groups.append(all_space)

        # print('y_coords:', y_coords, ', x_coords:', x_coords)
        # print('ht_eg_y_coords:', ht_eg_y_coords, ', ht_eg_x_coords:',
        #       ht_eg_x_coords)
        # y_max = border_y.max()
        # new_outside_space.append(outside_space)
    # print('len(new_inside_groups):', len(new_inside_groups))
    # print('len(new_border_groups):', len(new_border_groups))
    # print('len(new_outside_space):', len(new_outside_space))

    # Add other outside space
    new_outside_space_groups = []
    for shape_no, _ in enumerate(new_inside_groups):
        # print('shape_no:', shape_no)
        a1 = all_space_groups[shape_no]
        b1 = new_inside_groups[shape_no]
        c1 = new_border_coords_groups[shape_no]
        new_outside_space_groups.append(
            all_space_groups[shape_no] - (new_inside_groups[shape_no] |
                                          new_border_coords_groups[shape_no]))
    # print('len(all_outside_space_groups):', len(all_outside_space_groups))

    # Filter outside space to within small range of outside box of shape
    for shape_no, _ in enumerate(new_inside_groups):
        all_space_y = (
            np.array([a_space[0] for a_space in new_border_groups[shape_no]]))
        all_space_x = (
            np.array([a_space[1] for a_space in new_border_groups[shape_no]]))
        rows, cols = (max(all_space_y) + 1), (max(all_space_x) + 1)
        new_outside_space = {os for os in new_outside_space_groups[shape_no]
                             if (os[0] >= -1 and os[0] <= rows and
                                 os[1] >= -1 and os[1] <= cols)}
        new_outside_space_groups[shape_no] = new_outside_space.copy()

    return (new_inside_groups, new_border_groups, new_corner_keeper_groups,
            new_outside_space_groups)


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


def clean_matrix_shapes(matrix,
                        matrix_shapes,
                        inside_groups,
                        corner_keeper_groups,
                        outside_spaces_groups):
    # print('inside_groups:', inside_groups)
    rows, cols = matrix.shape
    cleaned_matrix_shapes = []
    horiz_sym = ('-', '+')
    vert_sym = ('|', '+')
    for shape_no, a_matrix_shape in enumerate(matrix_shapes):
        print('looking at shape:\n', a_matrix_shape)
        # print('inside_group:', inside_groups[shape_no])
        rows, cols = a_matrix_shape.shape
        this_inside_group = inside_groups[shape_no]
        this_ht_end_group = corner_keeper_groups[shape_no]
        this_outside_space = outside_spaces_groups[shape_no]
        # print('this_ht_end_group:', this_ht_end_group)
        print('this_outside_space:', this_outside_space)
        intersections = list(zip(*[list(x)
                                   for x in np.where(a_matrix_shape == '+')]))
        print('intersections:', intersections)
        for intersect in intersections:
            # intersect = list(intersect)
            print('intersect:', intersect)
            y_coord, x_coord = intersect
            if (y_coord, x_coord) in this_ht_end_group:
                continue
            x_pre = x_coord - 1
            x_0_5_pre = x_coord - 0.5
            x_post = x_coord + 1
            x_0_5_post = x_coord + 0.5
            y_pre = y_coord - 1
            y_0_5_pre = y_coord - 0.5
            y_post = y_coord + 1
            y_0_5_post = y_coord + 0.5
            m10 = a_matrix_shape[y_coord, x_pre] if x_pre >= 0 else 'x'
            m12 = a_matrix_shape[y_coord, x_post] if x_post < cols else 'x'
            # m00 = (a_matrix_shape[y_pre, x_pre]if (y_pre >= 0 and x_pre >= 0)
            #        else '')
            # m01 = a_matrix_shape[y_pre, x_coord] if y_pre >= 0 else 'x'


            m01 = (' ' if (y_pre, x_coord) in this_outside_space else
                   (a_matrix_shape[y_pre, x_coord] if y_pre >= 0 else ' '))

            # m02 = (a_matrix_shape[y_pre, x_post]
            #        if (y_pre >= 0 and x_post < cols) else 'x')
            # m20 = (a_matrix_shape[y_post, x_pre]
            #        if (y_post < rows and x_pre > 0) else 'x')
            m21 = a_matrix_shape[y_post, x_coord] if y_post < rows else 'x'
            # m22 = (a_matrix_shape[y_post, x_post]
            #        if (y_post < rows and x_post < cols) else '')
            # m0_50 = ' ' if (y_0_5_pre, x_pre) in this_inside_group else 'z'
            # m0_51 = ' ' if (y_0_5_pre, x_coord) in this_inside_group else 'z'


            m0_51 = (' ' if (y_0_5_pre, x_coord) in this_outside_space else
                     ' ' if (y_0_5_pre, x_coord) in this_inside_group else'z')
            # m0_52 = ' ' if (y_0_5_pre, x_post) in this_inside_group else 'z'
            # m1_50 = ' ' if (y_0_5_post, x_pre) in this_inside_group else 'z'
            m1_51 = ' ' if (y_0_5_post, x_coord) in this_inside_group else 'z'
            # m1_52 = ' ' if (y_0_5_post, x_post) in this_inside_group else 'z'

            # m00_5 = ' ' if (y_pre, x_0_5_pre) in this_inside_group else 'z'
            m10_5 = ' ' if (y_coord, x_0_5_pre) in this_inside_group else 'z'
            # m20_5 = ' ' if (y_post, x_0_5_pre) in this_inside_group else 'z'
            # m01_5 = ' ' if (y_pre, x_0_5_post) in this_inside_group else 'z'
            m11_5 = ' ' if (y_coord, x_0_5_post) in this_inside_group else 'z'
            # m21_5 = ' ' if (y_post, x_0_5_post) in this_inside_group else 'z'

            # Looking for Horizontal non-intersections to replace
            if m10 in horiz_sym and m12 in horiz_sym:
                print('found a potential horiz. non-intersection')
                if ((m01 == ' ' or m0_51 == ' ') and
                        (m21 in ' x' or m1_51 in ' x')):
                    print('yup - 1')
                    a_matrix_shape[intersect] = '-'
                elif ((m21 == ' ' or m1_51 == ' ') and
                        (m01 in ' x' or m0_51 in ' x')):
                    # print('replacing at intersect:', intersect, ', -')
                    print('yup - 2')
                    a_matrix_shape[intersect] = '-'
                else:
                    pass
                    print('not replacing horiz. at intersect:', intersect)

            # Looking for Vertical non-intersetions to replace
            if m01 in vert_sym and m21 in vert_sym:
                print('found a potential vert. non-intersection')
                # if ((m00 == ' ' and m10 == ' ' and m20 == ' ') or
                if ((m10 == ' ' or m10_5 == ' ') and
                        (m12 in ' x' or m11_5 in ' x')):
                    print('yup - 1')
                    a_matrix_shape[intersect] = '|'
                elif ((m12 == ' ' or m11_5 == ' ') and
                      (m10 in ' x' or m10_5 in ' x')):
                    # print('replacing at intersect:', intersect, ', |')
                    print('yup - 2')
                    a_matrix_shape[intersect] = '|'
                else:
                    pass
                    print('not replacing vert. at intersect:', intersect)
            else:
                pass
                # print('no replacement')
            # print('intersect:', intersect)
            # print('list(intersect):', list(intersect))
            # print('corner_keeper_groups[shape_no]:',
            #       corner_keeper_groups[shape_no])

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
        shapes = {}
        answers = {}
        # Test 1 - Simple shape
        shapes[1] = """
+----------+
|          |
|          |
|          |
+----------+
|          |
|          |
+----------+
""".strip('\n')
        answers[1] = ["""
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

        shapes[2] = """
+------------+
|            |
|            |
|            |
+------+-----+
|      |     |
|      |     |
+------+-----+
""".strip('\n')

        answers[2] = ["""
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

        shapes[3] = """
+-------------------+--+
|                   |  |
|                   |  |
|  +----------------+  |
|  |                   |
|  |                   |
+--+-------------------+
""".strip('\n')
        answers[3] = ["""
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

        shapes[4] = """
                           
                           
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
        answers[4] = ["""
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
""".strip('\n')]

        shapes[5] = """
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
        answers[5] = [shapes[5]]

        shapes[6] = """
+------------+
|            |
|            |
|            |
+------++----+
|      ||    |
|      ||    |
+------++----+
""".strip('\n')

        answers[6] = ["""
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

        shapes[8] = """
+----++----++----++----+
+----++----++----++----+
""".strip('\n')
        answers[8] = ["""
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

        shapes[9] = """
+-------------------++--+
|                   ||  |
|                   ||  |
|  +----------------+|  |
|  |+----------------+  |
|  ||                   |
+--++-------------------+
""".strip('\n')
        answers[9] = ["""
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

        shapes[10] = """
""".strip('\n')
        answers[10] = []

        shapes[11] = """
+-----+
+----+|
|+--+||
||++|||
||++|||
||+-+||
|+---+|
+-----+
""".strip('\n')
        answers[11] = ["""
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

        shapes[12] = """
          
 +-----+ 
 +----+| 
 |+--+|| 
 ||++||| 
 ||++||| 
 ||+-+|| 
 |+---+| 
 +-----+ 
""".strip('\n')
        answers[12] = ["""
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

        shapes[13] = """
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
        answers[13] = [shapes[13]]

        shapes[14] = """
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
        answers[14] = [
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

        shapes[75] = """
  +-----------------+
  |+--------++-----+|
  ||        ++     ||
  |+--------+|     ||
+++----------+     ||
|++----------------+|
|||+----------------+
||||
|||+------+
||+-------+
|+--------+
+---------+

+-----------+
|+++------++|
||++      ++|
||        |||
|+--------+||
+----------+|
+-----------+
""".strip('\n')
        answers[75] = [
"""
           +-----+
           |     |
           |     |
+----------+     |
+----------------+
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
++
++
""".strip('\n'),
"""
++
++
""".strip('\n'),
"""
++
||
||
||
|+-------+
+--------+
""".strip('\n'),
"""
++
||
||
||
||
||
|+--------+
+---------+
""".strip('\n'),
"""
+++------+
|++      |
|        |
+--------+
""".strip('\n'),
"""
+--------+
|        |
+--------+
""".strip('\n'),
"""
+-----------+
|+---------+|
||        ++|
||        |||
|+--------+||
+----------+|
+-----------+
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

        shapes[67] = """
+----+
|    |
|    +----+
|    |    |
|    +---+|
|    |   ||
|+---+   ||
||       ||
|+-------+|
+---------+
""".strip('\n')
        answers[67] = [
"""
    +---+
    |   |
+---+   |
|       |
+-------+
""".strip('\n'),
"""
+----+
|    |
|    +----+
|    |    |
|    +---+|
|    |   ||
|+---+   ||
||       ||
|+-------+|
+---------+
""".strip('\n')]

        shapes[77] = """
+-----+
|     +--+
+----+   +---+
     |       |
     +---+ +-+
         | |
         | |
         | |
         +-+
""".strip('\n')
        answers[77] = [
"""
+-----+
|     +--+
+----+   +---+
     |       |
     +---+ +-+
         | |
         | |
         | |
         +-+
""".strip('\n')]

        for a_test_no in sorted(shapes, key=lambda x: int(x)):

            if a_test_no != 75:
                continue

            print(''.join(['Test ', str(a_test_no), ': ']), end='')
            shape = shapes[a_test_no]
            result = break_evil_pieces(shape)
            answer = answers[a_test_no]
            result_counter = collections.Counter(result)
            answer_counter = collections.Counter(answer)
            pass_result = result_counter == answer_counter
            if not pass_result:
                print('\n'.join(['\nshape:', shape]))
                print('\n'.join(['\nresult:', '\n\n'.join(result)]))
                print('\n'.join(['\nanswer:', '\n\n'.join(answer)]))
                missing_answers = []
                for an_answer in answer_counter:
                    if (answer_counter[an_answer] >
                            result_counter.get(an_answer, 0)):
                        missing_answers.append(an_answer)
                print('\n'.join(['\nType of shapes that your answer was ' +
                                 'missing:'] + missing_answers))
                extra_results = []
                for a_result in result_counter:
                    if result_counter[a_result] > answer_counter.get(a_result,
                                                                     0):
                        extra_results.append(a_result)
                print('\n'.join(['\nType of shapes that your solution ' +
                                 "shouldn't return:"] + extra_results))
            self.assertTrue(pass_result)
            print('correct!')


if __name__ == '__main__':
    unittest.main()

"""
Result:

"""
