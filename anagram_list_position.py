# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 21:01:58 2019

@author: PaulJ
"""

import unittest

from collections import Counter
from math import factorial
from operator import mul  # reduce(mul, list)
from functools import reduce


def listPosition(word):
    """Return the anagram list position of the word"""
    word_one = sorted(word)
    chars_remaining = list(word_one)
    word_pos = 1
    for a_char in word:
        a_char_pos = chars_remaining.index(a_char)
        preceding_chars = chars_remaining[:a_char_pos]
        unique_pre_chars = list(set(preceding_chars))
        remaining_chars = len(chars_remaining)
        for a_uniq_pre_char in unique_pre_chars:
            remain_chars = chars_remaining[:]
            remain_chars.remove(a_uniq_pre_char)
            rem_char_count = Counter(remain_chars)
            rem_char_count_gt_1 = [x for x in rem_char_count.values()
                                   if x > 1]
            rem_char_cou_fact_prod = (reduce(
                mul, [factorial(x) for x in rem_char_count_gt_1])
                if rem_char_count_gt_1 else 1)

            remain_pre_chars = preceding_chars[:]
            remain_pre_chars.remove(a_uniq_pre_char)

            word_pos += (factorial(remaining_chars - 1) //
                         rem_char_cou_fact_prod)
        chars_remaining.remove(a_char)
    return word_pos


class InterpreterTestMethods(unittest.TestCase):

    tests = {'QUESTION': 24572,
             'BOOKKEEPER': 10743,
             'A': 1,
             'BAAA': 4,
             'ABAB': 2,
             'AAAB': 1,
             'IMMUNOELECTROPHORETICALLY': 718_393_983_731_145_698_173,
             # not                        718_393_983_731_145_768_960
             'AMHEVJUXGMKWWDMXBTCIINGAP': 3_485_013_467_205_603_370_503,
             # not                        3_485_013_467_205_605_523_456
             'BBDKWZIUEPUWZENRQSPAW': 14_023_220_199_797_223,
             # not                    14_023_220_199_797_222 
             'OEUUAMEEQEVZQJRYKHLSGVEPV': 2_628_242_505_275_145_177_799,
             # not                        2_628_242_505_275_147_288_576
             }

    def test_basic(self):
        for word in self.tests:
            answer = self.tests[word]
            result = listPosition(word)
            print('word:', word, ', answer:', answer,
                  ', result:', result)
            self.assertEqual(result, answer)


if __name__ == '__main__':
    unittest.main()
