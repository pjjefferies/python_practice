# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 22:54:53 2019

@author: PaulJ
"""

def perimeter(n):
    total = 0
    last = 1
    next_last = 0
    while n >= 0:
        total += last
        last, next_last = last + next_last, last
        n -= 1
    return total * 4
