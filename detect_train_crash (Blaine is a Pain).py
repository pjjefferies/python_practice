# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 23:45:01 2019

@author: PaulJ
"""

import unittest
from collections import Counter


def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    a_track = Track(track)
    train_a = Train(a_train, a_train_pos)
    train_b = Train(b_train, b_train_pos)
    a_track.add_train(train_a)
    a_track.add_train(train_b)

    for time in range(limit + 1):
        if a_track.detect_crash():
            return time
        a_track.time_increment()
    return -1


class Track_space():
    def __init__(self, shape, dir_in, x_loc, y_loc):
        self.x = x_loc
        self.y = y_loc
        self.dir_in = dir_in
        self.station = shape == 'S'


class Track():
    def __init__(self, track_str):
        self.track_matrix = [[x for x in row]
                             for row in track_str.strip('\n').split('\n')]
        self.start = self.track_matrix[0].index('/'), 0
        self.track_seq = [Track_space('/', 'e', *self.start)]
        self.trains = []
        height = len(self.track_matrix) + 1
        width = max([len(row) for row in self.track_matrix]) + 1
        self.track_matrix.append(' ' * (width))
        for row_no in range(height):
            self.track_matrix[row_no] += (
                ' ' * (width - len(self.track_matrix[row_no])))
        self.track_matrix.append(' ' * (width))
        new_x, new_y = None, None

        while (new_x != self.start[0] or new_y != self.start[1]):
            la_tr_sp_dir = self.track_seq[-1].dir_in
            la_tr_sp_x = self.track_seq[-1].x
            la_tr_sp_y = self.track_seq[-1].y
            if la_tr_sp_dir == 'sw':
                if (self.track_matrix[la_tr_sp_y][la_tr_sp_x - 1]
                        in ('-', 'S', '+')):
                    new_x = la_tr_sp_x - 1
                    new_y = la_tr_sp_y
                    new_dir = 'w'
                elif (self.track_matrix[la_tr_sp_y + 1][la_tr_sp_x - 1]
                        in ('/', 'S', 'X')):
                    new_x = la_tr_sp_x - 1
                    new_y = la_tr_sp_y + 1
                    new_dir = 'sw'
                elif (self.track_matrix[la_tr_sp_y + 1][la_tr_sp_x]
                        in ('|', 'S', '+')):
                    new_x = la_tr_sp_x
                    new_y = la_tr_sp_y + 1
                    new_dir = 's'
                else:
                    raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                     ', ' + str(la_tr_sp_y + 1) +
                                     ' not valid')
            elif la_tr_sp_dir == 's':
                if (self.track_matrix[la_tr_sp_y + 1][la_tr_sp_x]
                        in ('/', '|', '\\', 'S', '+')):
                    new_x = la_tr_sp_x
                    new_y = la_tr_sp_y + 1
                    if (self.track_matrix[la_tr_sp_y + 1][la_tr_sp_x]
                            in ('|', 'S', '+')):
                        new_dir = 's'
                    elif (self.track_matrix[la_tr_sp_y + 1]
                          [la_tr_sp_x] == '/'):
                        new_dir = 'sw'
                    elif (self.track_matrix[la_tr_sp_y+1][la_tr_sp_x] == '\\'):
                        new_dir = 'se'
                    else:
                        raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                         ', ' + str(la_tr_sp_y + 1) +
                                         ' not valid')
                else:
                    raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                     ', ' + str(la_tr_sp_y + 1) +
                                     ' not valid')
            elif la_tr_sp_dir == 'se':
                if (self.track_matrix[la_tr_sp_y][la_tr_sp_x + 1]
                        in ('-', 'S', '+')):
                    new_x = la_tr_sp_x + 1
                    new_y = la_tr_sp_y
                    new_dir = 'e'
                elif (self.track_matrix[la_tr_sp_y + 1][la_tr_sp_x + 1]
                        in ('\\', 'S', 'X')):
                    new_x = la_tr_sp_x + 1
                    new_y = la_tr_sp_y + 1
                    new_dir = 'se'
                elif (self.track_matrix[la_tr_sp_y + 1][la_tr_sp_x]
                        in ('|', 'S', '+')):
                    new_x = la_tr_sp_x
                    new_y = la_tr_sp_y + 1
                    new_dir = 's'
                else:
                    raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                     ', ' + str(la_tr_sp_y + 1) +
                                     ' not valid')
            elif la_tr_sp_dir == 'e':
                if (self.track_matrix[la_tr_sp_y][la_tr_sp_x + 1]
                        in ('/', '-', '\\', 'S', '+')):
                    new_x = la_tr_sp_x + 1
                    new_y = la_tr_sp_y
                    if (self.track_matrix[la_tr_sp_y][la_tr_sp_x + 1]
                            in ('-', 'S', '+')):
                        new_dir = 'e'
                    elif (self.track_matrix[la_tr_sp_y]
                          [la_tr_sp_x + 1] == '/'):
                        new_dir = 'ne'
                    elif (self.track_matrix[la_tr_sp_y][la_tr_sp_x+1] == '\\'):
                        new_dir = 'se'
                    else:
                        raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                         ', ' + str(la_tr_sp_y + 1) +
                                         ' not valid')
                else:
                    raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                     ', ' + str(la_tr_sp_y + 1) +
                                     ' not valid')
            elif la_tr_sp_dir == 'ne':
                if (self.track_matrix[la_tr_sp_y][la_tr_sp_x + 1]
                        in ('-', 'S', '+')):
                    new_x = la_tr_sp_x + 1
                    new_y = la_tr_sp_y
                    new_dir = 'e'
                elif (self.track_matrix[la_tr_sp_y - 1][la_tr_sp_x + 1]
                        in ('/', 'S', 'X')):
                    new_x = la_tr_sp_x + 1
                    new_y = la_tr_sp_y - 1
                    new_dir = 'ne'
                elif (self.track_matrix[la_tr_sp_y - 1][la_tr_sp_x]
                        in ('|', 'S', '+')):
                    new_x = la_tr_sp_x
                    new_y = la_tr_sp_y - 1
                    new_dir = 'n'
                else:
                    raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                     ', ' + str(la_tr_sp_y + 1) +
                                     ' not valid')
            elif la_tr_sp_dir == 'n':
                if (self.track_matrix[la_tr_sp_y - 1][la_tr_sp_x]
                        in ('/', '|', '\\', 'S', '+')):
                    new_x = la_tr_sp_x
                    new_y = la_tr_sp_y - 1
                    if (self.track_matrix[la_tr_sp_y - 1][la_tr_sp_x]
                            in ('|', 'S', '+')):
                        new_dir = 'n'
                    elif (self.track_matrix[la_tr_sp_y - 1]
                          [la_tr_sp_x] == '/'):
                        new_dir = 'ne'
                    elif (self.track_matrix[la_tr_sp_y-1][la_tr_sp_x] == '\\'):
                        new_dir = 'nw'
                    else:
                        raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                         ', ' + str(la_tr_sp_y + 1) +
                                         ' not valid')
                else:
                    raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                     ', ' + str(la_tr_sp_y + 1) +
                                     ' not valid')
            elif la_tr_sp_dir == 'nw':
                if (self.track_matrix[la_tr_sp_y][la_tr_sp_x - 1]
                        in ('-', 'S', '+')):
                    new_x = la_tr_sp_x - 1
                    new_y = la_tr_sp_y
                    new_dir = 'w'
                elif (self.track_matrix[la_tr_sp_y - 1][la_tr_sp_x - 1]
                        in ('\\', 'S', 'X')):
                    new_x = la_tr_sp_x - 1
                    new_y = la_tr_sp_y - 1
                    new_dir = 'nw'
                elif (self.track_matrix[la_tr_sp_y - 1][la_tr_sp_x]
                        in ('|', 'S', '+')):
                    new_x = la_tr_sp_x
                    new_y = la_tr_sp_y - 1
                    new_dir = 'n'
                else:
                    raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                     ', ' + str(la_tr_sp_y + 1) +
                                     ' not valid')
            elif la_tr_sp_dir == 'w':
                if (self.track_matrix[la_tr_sp_y][la_tr_sp_x - 1]
                        in ('/', '-', '\\', 'S', '+')):
                    new_x = la_tr_sp_x - 1
                    new_y = la_tr_sp_y
                    if (self.track_matrix[la_tr_sp_y][la_tr_sp_x - 1]
                            in ('-', 'S', '+')):
                        new_dir = 'w'
                    elif (self.track_matrix[la_tr_sp_y]
                          [la_tr_sp_x - 1] == '/'):
                        new_dir = 'sw'
                    elif (self.track_matrix[la_tr_sp_y][la_tr_sp_x-1] == '\\'):
                        new_dir = 'nw'
                    else:
                        raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                         ', ' + str(la_tr_sp_y + 1) +
                                         ' not valid')
                else:
                    raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                     ', ' + str(la_tr_sp_y + 1) +
                                     ' not valid')
            else:
                    raise ValueError('Track at space: ' + str(la_tr_sp_x) +
                                     ', ' + str(la_tr_sp_y + 1) +
                                     ' not valid')
            self.track_seq.append(Track_space(self.track_matrix[new_y][new_x],
                                              new_dir,
                                              new_x, new_y))
        self.track_seq = self.track_seq[:-1]
        self.steps = len(self.track_seq)

    def add_train(self, train):
        self.trains.append(train)

    def time_increment(self):
        # move trains
        for a_train_no, a_train in enumerate(self.trains):
            if not self.trains[a_train_no].station_delay:
                self.trains[a_train_no].pos = (
                    (self.trains[a_train_no].pos + a_train.incr) % self.steps)
                if (not a_train.express and
                        self.track_seq[a_train.pos].station):
                    # print('stopped at station')
                    self.trains[a_train_no].station_delay = (a_train.length -
                                                             1)
            else:
                self.trains[a_train_no].station_delay = (
                    self.trains[a_train_no].station_delay - 1)

    def detect_crash(self):
        train_pos = []
        for a_train in self.trains:
            for a_train_car_no in range(a_train.length):
                a_train_car_pos = ((a_train.pos +
                                    a_train_car_no * a_train.car_incr) %
                                   self.steps)
                train_pos.append((self.track_seq[a_train_car_pos].x,
                                  self.track_seq[a_train_car_pos].y))

        return max(Counter(train_pos).values()) > 1


class Train():
    def __init__(self, train_str, start_pos):
        self.train_str = train_str
        self.start_pos = start_pos
        if train_str[0].isupper():
            self.incr = -1
            self.car_incr = 1
            self.express = train_str[0] == 'X'
        elif train_str[-1].isupper():
            self.incr = 1
            self.car_incr = -1
            self.express = train_str[-1] == 'X'
        else:
            raise ValueError('Train must have an engine')
        self.station_delay = 0
        self.length = len(train_str)
        self.pos = start_pos


class TestMethods(unittest.TestCase):

    TRACK_EX1 = """\
                                /------------\\
/-------------\\                /             |
|             |               /              S
|             |              /               |
|        /----+--------------+------\\        |   
\\       /     |              |      |        |     
 \\      |     \\              |      |        |                    
 |      |      \\-------------+------+--------+---\\
 |      |                    |      |        |   |
 \\------+--------------------+------/        /   |
        |                    |              /    | 
        \\------S-------------+-------------/     |
                             |                   |
/-------------\\              |                   |
|             |              |             /-----+----\\
|             |              |             |     |     \\
\\-------------+--------------+-----S-------+-----/      \\
              |              |             |             \\
              |              |             |             |
              |              \\-------------+-------------/
              |                            |               
              \\----------------------------/ 
"""

    TRACK_EX2 = """\
/-------\\ 
|       | 
|       | 
|       | 
\\-------+--------\\
        |        |
        S        |
        |        |
        \\--------/
"""


    tests = {(TRACK_EX1, "Aaaa", 147, "Bbbbbbbbbbb", 288, 1000): 516,
             (TRACK_EX2, "aaaA", 22, "bbbbB", 0, 16): 16
             }

    def test_basic(self):
        for params in self.tests:
            answer = self.tests[params]
            result = train_crash(*params)
            if result != answer:
                print('\nwrong: params:', params, ', answer:',
                      answer, ', result:', result)
            else:
                print('\ncorrect!')
                pass
            self.assertEqual(result, answer)


if __name__ == '__main__':
    unittest.main()

"""
Result:

"""
