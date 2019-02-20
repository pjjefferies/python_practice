# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 23:14:52 2019

@author: PaulJ
"""

import unittest


def elder_age(m, n, l, t):
    pass


class TestMethods(unittest.TestCase):

    tests = {(8, 5, 1, 100): 5,
             (8, 8, 0, 100007): 224,
             (25, 31, 0, 100007): 11925,
             (5, 45, 3, 1000007): 4323,
             (28827050410, 35165045587, 7109602, 13719506): 5456283}

    def test_basic(self):
        for params in self.tests:
            answer = self.tests[params]
            result = elder_age(*params)
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
