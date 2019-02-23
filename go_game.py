# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 23:39:34 2019

@author: PaulJ
"""

import unittest
import numpy as np

class Go():
    def __init__(self, height=False, width=False):
        try:
            if not height or int(height) != height:
                raise ValueError('Height must be supplied as an integer')
            if width:
                try:
                    if int(width) != width:
                        raise ValueError(
                            'If supplied, width must be an integer')
                except ValueError:
                    raise ValueError('If supplied, width must be an integer')
        except ValueError:
            raise ValueError('Height must be supplied as an integer')
        self.height = height
        if width:
            self.width = width
        else:
            self.width = height
        self.boards = [np.full((self.height, self.width), '.')]
        self.blacks_turn = True

    def board(self):
        # return str(self)  # this is what decription wants but not tests
        return self.boards[-1].tolist()

    def move(self, *move_str):
        print('move_str:', move_str, ', len(move_str):', len(move_str))
        if len(move_str) > 1:
            for a_move_str in move_str:
                self.move(a_move_str)
        self.boards.append(self.boards[-1])
        self.pass_turn()

    def handicap_stones(self, no_hc_stones):
        pass

    def size(self):
        return {'height': self.height,
                'width': self.width}

    def rollback(self, no_steps=None):
        if no_steps is None:
            raise ValueError('Number of steps to roll back must be supplied')
        elif not isinstance(no_steps, int):
            raise ValueError('Number of steps to roll back must be an integer')
        elif no_steps > (len(self.boards) - 1):
            raise ValueError('Number of roll back steps, ' + str(no_steps) +
                             ', cannot be larger than the number of steps ' +
                             'taken so far, ' + str(len(self.boards)-1))
        self.boards = self.boards[-no_steps]

    def get_position(self, pos_str):
        pass

    def turn(self):
        return 'black' if self.blacks_turn else 'white'

    def pass_turn(self):
        self.blacks_turn = not self.blacks_turn

    def _board_pos(self, board_pos_str):
        if not (board_pos_str is isinstance(str)):
            raise ValueError('Board Position must be supplied')
        try:
            row_str = board_pos_str[:-1]
            col_str = board_pos_str[-1]
            row = self.height - int(row_str)
            col = 'ABCDEFGHJKLMONPQRSTUVWXYZ'.index(col_str)
            return (col, row)  # (x, y)
        except ValueError:
            raise ValueError('Board Position must be of form "A1"')

    def _detect_captured_stones(self):
        pass

    def _remove_captured_stones(self, stones):
        pass

    def __str__(self):
        return '\n'.join([''.join([ele for ele in row])
                          for row in self.boards[-1]])


class TestMethods(unittest.TestCase):

    # tests = {1: [(9, 16), lambda: game.size(), ]}

    def test_basic(self):
        # Test 1
        game = Go(9, 16)
        result = game.size()
        answer = {"height": 9, "width": 16}
        if result != answer:
            print('\nwrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('Test 1 correct!')
        self.assertEqual(result, answer)

        # Test 2
        game = Go(9)
        game.move("3B")
        result = game.turn()
        answer = 'white'
        if result != answer:
            print('\nwrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('Test 2A correct!')
        self.assertEqual(game.turn(), 'white')
        game.move("4B")
        result = game.turn()
        answer = 'black'
        if result != answer:
            print('\nwrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('Test 2B correct!')
        self.assertEqual(game.turn(), 'black')

        # Test 3
        game = Go(9)
        board = [[".",".",".",".",".",".",".",".","."],
                 [".",".",".",".",".",".",".",".","."],
                 [".",".",".",".",".",".",".",".","."],
                 [".",".",".",".",".",".",".",".","."],
                 [".",".",".",".",".",".",".",".","."],
                 [".",".",".",".",".",".",".",".","."],
                 [".",".",".",".",".",".",".",".","."],
                 [".",".",".",".",".",".",".",".","."],
                 [".",".",".",".",".",".",".",".","."]]
        game.move("3B","2B","1B")
        game.rollback(3)
        result = game.board()
        answer = board
        if result != answer:
            print('\nwrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('Test 3A correct!')
        self.assertEqual(game.board(), board)
        result = game.turn()
        answer = 'black'
        if result != answer:
            print('\nwrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('Test 3B correct!')

        self.assertEqual(game.turn(), "black")


if __name__ == '__main__':
    unittest.main()

"""
Result:

"""
