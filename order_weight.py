# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 00:47:42 2019

@author: PaulJ
"""


def order_weight(strng):
    return ''.join([
        x for x in sorted(sorted(strng.split()),
                          key=lambda num_str: sum(
                              int(a_letter) for a_letter in num_str))])
