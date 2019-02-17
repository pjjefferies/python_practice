# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 23:39:45 2019

@author: PaulJ
"""


def scramble(s1, s2):
    s1_dict = {}
    for a_char in s1:
        s1_dict[a_char] = s1_dict.get(a_char, 0) + 1

    s2_dict = {}
    for a_char in s2:
        s2_dict[a_char] = s2_dict.get(a_char, 0) + 1

    for a_char in s2_dict:
        if s1_dict.get(a_char, 0) < s2_dict[a_char]:
            return False

    return True