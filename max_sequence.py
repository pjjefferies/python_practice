# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 23:09:53 2019

@author: PaulJ
"""

import random

def maxSequence(arr):
    # begin_max_seq = 0
    # end_max_seq = 0
    max_seq_sum = 0
    for a_beg_dig_no, _ in enumerate(arr):
        print('second loop range:', list(range(a_beg_dig_no+1,len(arr)+1)))
        for an_end_dig_no in range(a_beg_dig_no+1,len(arr)+1):
            this_sum = sum(arr[a_beg_dig_no:an_end_dig_no])
            if this_sum > max_seq_sum:
                max_seq_sum = this_sum
                # begin_max_seq = a_beg_dig_no
                # end_max_seq = an_end_dig_no
            print(a_beg_dig_no, an_end_dig_no, this_sum, max_seq_sum)
    return max_seq_sum




"""
for no_values in range(100):
    values = []
    for a_value_pos in range(no_values):
        values.append(random.randint(-100,100))
"""


print('maxSequence([-2, 1, -3, 4, -1, 2, 1, -5, 4]):', 
      maxSequence([-2, 1, -3, 4, -1, 2, 1, -5, 4]), '= 6 ?')