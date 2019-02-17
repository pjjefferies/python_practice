# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 11:19:33 2019

@author: PaulJ
"""


def path_finder(area):
    area = [[int(x) for x in y] for y in area.split('\n')]
    area_width = len(area[0])
    area_depth = len(area)
    dist_min = [[1e10 for _ in range(area_width)]
                for _ in range(area_depth)]
    dist_min[0][0] = 0
    space_check_queue = [(0, 0)]
    while space_check_queue:
        curr_y, curr_x = space_check_queue.pop(0)
        current_sq_climb = dist_min[curr_y][curr_x]
        current_alt = area[curr_y][curr_x]

        for delta_x, delta_y in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            new_x = curr_x + delta_x
            new_y = curr_y + delta_y
            if (new_x >= area_width or
                new_x < 0 or
                new_y >= area_depth or
                    new_y < 0):
                continue

            new_dist = (current_sq_climb +
                        abs(current_alt - area[new_y][new_x]))
            if new_dist < dist_min[new_y][new_x]:
                dist_min[new_y][new_x] = new_dist
                space_check_queue.append((new_y, new_x))

    return dist_min[area_depth-1][area_width-1]


a = "\n".join([
  "000",
  "000",
  "000"
])

b = "\n".join([
  "010",
  "010",
  "010"
])

c = "\n".join([
  "010",
  "101",
  "010"
])

d = "\n".join([
  "0707",
  "7070",
  "0707",
  "7070"
])

e = "\n".join([
  "700000",
  "077770",
  "077770",
  "077770",
  "077770",
  "000007"
])

f = "\n".join([
  "777000",
  "007000",
  "007000",
  "007000",
  "007000",
  "007777"
])

g = "\n".join([
  "000000",
  "000000",
  "000000",
  "000010",
  "000109",
  "001010"
])

h = '\n'.join([
  '07000',
  '07070',
  '07070',
  '07070',
  '07070',
  '00070'
])
