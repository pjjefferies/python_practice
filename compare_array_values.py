# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 23:52:00 2019

@author: PaulJ
"""

def comp(array1, array2):
    if (not isinstance(array1, list) or not isinstance(array2, list)) and array1 != array2:
        return False
    for an_array1_value in array1:
        if an_array1_value ** 2 not in array2:
            return False
    for an_array2_value in array2:
        if an_array2_value ** 0.5 not in array1:
            return False
    return True


a = [12, 90, 76, 95, 12, 45, 58]
b = [145, 8100, 5776, 9025, 144, 2025, 3364]

print(comp(a, b))

print([x**2 for x in a])
