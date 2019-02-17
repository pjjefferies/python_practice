# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 21:15:06 2019

@author: PaulJ
"""

from copy import deepcopy


def longest_slide_down(pyramid):
    max_sum = deepcopy(pyramid)
    for a_lev_no, a_lev in reversed(list(enumerate(max_sum[:-1]))):
        for a_h_pos_no, _ in enumerate(a_lev):
            max_sum[a_lev_no][a_h_pos_no] = (
                max(max_sum[a_lev_no+1][a_h_pos_no],
                    max_sum[a_lev_no+1][a_h_pos_no + 1]) +
                max_sum[a_lev_no][a_h_pos_no])

    return max_sum[0][0]