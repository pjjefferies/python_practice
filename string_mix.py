# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 09:48:05 2019

@author: PaulJ
"""

from collections import Counter


def mix(s1, s2):
    lower_case_counter = Counter('abcdefghijklmnopqrstuvwxyz' * 1000)
    s1_counter = Counter(s1) & lower_case_counter
    s2_counter = Counter(s2) & lower_case_counter

    both_counters = s1_counter | s2_counter

    list_of_chars = [(a_let, a_let_count)
                     for a_let, a_let_count in both_counters.most_common()
                     if a_let_count > 1]

    letter_string_count = Counter({a_let: a_let_count for a_let, a_let_count
                                   in both_counters.items()
                                   if a_let_count > 1})

    letter_string_source = {
        a_let: '1:' if s1_counter[a_let] > s2_counter[a_let]
               else ('2:' if s1_counter[a_let] < s2_counter[a_let]
                     else '=:')
               for a_let, _ in letter_string_count.items()}

    letter_string_list = [letter_string_source[a_let] +
                          a_let * a_let_count
                          for a_let, a_let_count in list_of_chars]

    letter_string_list = sorted(letter_string_list,
                                key=lambda x: (-letter_string_count[x[-1]],
                                               x))

    result_string = '/'.join(letter_string_list)

    return result_string