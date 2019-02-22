# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 23:39:34 2019

@author: PaulJ
"""

import unittest


class go():
    def __init__(self, height, width=False):
        self.height = height
        if width:
            self.width = width
        else:
            width = height
        pass

    def board(self):
        print(self)

    def move(self, move_str):
        pass

    def handicap_stones(self, no_hc_stones):
        pass

    def size(self):
        pass

    def rollback(self, no_steps):
        pass

    def get_position(self, pos_str):
        pass

    def turn(self):
        pass

    def pass_turn(self):
        pass

    def _detect_captured_stones(self):
        pass

    def _remove_captured_stones(self, stones):
        pass

    def __str__(self):
        return '\n'.join([])


class TestMethods(unittest.TestCase):

    tests = {}

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
