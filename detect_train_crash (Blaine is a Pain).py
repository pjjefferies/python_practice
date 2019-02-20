# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 23:45:01 2019

@author: PaulJ
"""

import unittest


def train_crash(track, a_train, a_train_pos, b_train, b_train_pos, limit):
    # Your code here!
    pass


def paramerterize_track(track):
    pass


class TestMethods(unittest.TestCase):

    TRACK_EX = """\
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

    tests = {(TRACK_EX, "Aaaa", 147, "Bbbbbbbbbbb", 288, 1000): 516
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
